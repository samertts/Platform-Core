from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

import pytest

from platform_core.runtime.events.engine import EventBus
from platform_core.runtime.types import Event, EventResult


class MockHandler:
    def __init__(self) -> None:
        self.events: list[Event] = []

    async def handle(self, event: Event) -> EventResult:
        self.events.append(event)
        return EventResult(success=True, handler="MockHandler")


class FailingHandler:
    async def handle(self, event: Event) -> EventResult:
        return EventResult(success=False, handler="FailingHandler", error="test error")


class TestEventBus:
    @pytest.mark.asyncio
    async def test_publish_subscribe(self) -> None:
        bus = EventBus()
        handler = MockHandler()
        bus.subscribe("test.event", handler)
        event = Event(type="test.event", source="test")
        await bus.publish(event)
        assert len(handler.events) == 1
        assert handler.events[0].type == "test.event"

    @pytest.mark.asyncio
    async def test_wildcard_subscribe(self) -> None:
        bus = EventBus()
        handler = MockHandler()
        bus.subscribe("*", handler)
        await bus.publish(Event(type="any.event", source="test"))
        assert len(handler.events) == 1

    @pytest.mark.asyncio
    async def test_unsubscribe(self) -> None:
        bus = EventBus()
        handler = MockHandler()
        sub_id = bus.subscribe("test.event", handler)
        bus.unsubscribe(sub_id)
        await bus.publish(Event(type="test.event", source="test"))
        assert len(handler.events) == 0

    @pytest.mark.asyncio
    async def test_dead_letter(self) -> None:
        bus = EventBus()
        bus.subscribe("test.event", FailingHandler())
        await bus.publish(Event(type="test.event", source="test"))
        dead = bus.get_dead_letters()
        assert len(dead) == 1
        assert bus.stats["dead_lettered"] == 1

    @pytest.mark.asyncio
    async def test_stats(self) -> None:
        bus = EventBus()
        handler = MockHandler()
        bus.subscribe("test.event", handler)
        await bus.publish(Event(type="test.event", source="test"))
        assert bus.stats["published"] == 1
        assert bus.stats["delivered"] == 1

    @pytest.mark.asyncio
    async def test_subscription_count(self) -> None:
        bus = EventBus()
        bus.subscribe("a", MockHandler())
        bus.subscribe("b", MockHandler())
        assert bus.subscription_count == 2

    def test_get_subscriptions(self) -> None:
        bus = EventBus()
        bus.subscribe("test.event", MockHandler())
        subs = bus.get_subscriptions("test.event")
        assert len(subs) == 1
