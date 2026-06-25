from __future__ import annotations

import asyncio
import logging
import threading
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Protocol, runtime_checkable
from uuid import uuid4

from platform_core.runtime.types import Event, EventResult

logger = logging.getLogger("platform_core.events")


@runtime_checkable
class EventHandler(Protocol):
    async def handle(self, event: Event) -> EventResult: ...


class Subscription:
    __slots__ = ("id", "event_type", "handler", "priority", "created_at")

    def __init__(
        self,
        subscription_id: str,
        event_type: str,
        handler: Any,
        priority: int = 50,
    ) -> None:
        self.id = subscription_id
        self.event_type = event_type
        self.handler = handler
        self.priority = priority
        self.created_at = datetime.now(timezone.utc)


class EventBus:
    """Async event bus with priority, dead-letter, and replay support."""

    def __init__(self, max_queue_size: int = 10000) -> None:
        self._subscriptions: dict[str, list[Subscription]] = defaultdict(list)
        self._dead_letters: list[Event] = []
        self._event_store: dict[str, list[Event]] = defaultdict(list)
        self._stats: dict[str, int] = {
            "published": 0,
            "delivered": 0,
            "failed": 0,
            "dead_lettered": 0,
        }
        self._lock = threading.RLock()
        self._max_queue_size = max_queue_size
        self._running = False
        self._queue: asyncio.Queue[Event] | None = None
        self._workers: list[asyncio.Task[None]] = []

    async def start(self) -> None:
        with self._lock:
            if self._running:
                return
            self._running = True
            self._queue = asyncio.Queue(maxsize=self._max_queue_size)

    async def stop(self) -> None:
        with self._lock:
            self._running = False
        for task in self._workers:
            task.cancel()
        self._workers.clear()

    async def publish(self, event: Event) -> None:
        with self._lock:
            self._stats["published"] += 1
            self._event_store[event.type].append(event)
            if len(self._event_store[event.type]) > 1000:
                self._event_store[event.type] = self._event_store[event.type][-500:]

        subscribers = list(self._subscriptions.get(event.type, []))
        wildcard_subscribers = list(self._subscriptions.get("*", []))
        all_subscribers = subscribers + wildcard_subscribers
        all_subscribers.sort(key=lambda s: s.priority, reverse=True)

        for subscription in all_subscribers:
            try:
                if asyncio.iscoroutinefunction(subscription.handler.handle):
                    result = await subscription.handler.handle(event)
                else:
                    result = subscription.handler.handle(event)

                if result.success:
                    with self._lock:
                        self._stats["delivered"] += 1
                else:
                    with self._lock:
                        self._stats["failed"] += 1
                        self._dead_letters.append(event)
                        self._stats["dead_lettered"] += 1
                        if len(self._dead_letters) > self._max_queue_size:
                            self._dead_letters = self._dead_letters[-self._max_queue_size:]
            except Exception as e:
                logger.error("Event handler error: %s", e)
                with self._lock:
                    self._stats["failed"] += 1
                    self._dead_letters.append(event)
                    self._stats["dead_lettered"] += 1

    def subscribe(self, event_type: str, handler: Any, priority: int = 50) -> str:
        subscription_id = str(uuid4())
        subscription = Subscription(subscription_id, event_type, handler, priority)
        with self._lock:
            self._subscriptions[event_type].append(subscription)
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        with self._lock:
            for event_type, subs in self._subscriptions.items():
                self._subscriptions[event_type] = [
                    s for s in subs if s.id != subscription_id
                ]

    async def replay(self, event_type: str, since: datetime | None = None) -> None:
        with self._lock:
            events = list(self._event_store.get(event_type, []))

        if since:
            events = [e for e in events if e.timestamp >= since]

        for event in events:
            await self.publish(event)

    def get_dead_letters(self, limit: int = 100) -> list[Event]:
        with self._lock:
            return list(self._dead_letters[-limit:])

    async def retry_dead_letter(self, event: Event) -> None:
        with self._lock:
            if event in self._dead_letters:
                self._dead_letters.remove(event)
        await self.publish(event)

    @property
    def stats(self) -> dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def subscription_count(self) -> int:
        with self._lock:
            return sum(len(subs) for subs in self._subscriptions.values())

    def get_subscriptions(self, event_type: str | None = None) -> list[dict[str, Any]]:
        with self._lock:
            if event_type:
                return [
                    {
                        "id": s.id,
                        "event_type": s.event_type,
                        "priority": s.priority,
                        "created_at": s.created_at.isoformat(),
                    }
                    for s in self._subscriptions.get(event_type, [])
                ]
            result = []
            for subs in self._subscriptions.values():
                for s in subs:
                    result.append(
                        {
                            "id": s.id,
                            "event_type": s.event_type,
                            "priority": s.priority,
                            "created_at": s.created_at.isoformat(),
                        }
                    )
            return result
