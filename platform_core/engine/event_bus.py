from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from platform_core.engine.events import EngineEvent, EngineEventType


class EventBus:
    """
    Lightweight synchronous event bus.

    Supports both:
      - Callables: handler(event)
      - Observer objects: handler.notify(event)
    """

    def __init__(self) -> None:
        self._handlers: dict[
            EngineEventType,
            list[Callable[[EngineEvent], Any] | Any],
        ] = defaultdict(list)

        self._global: list[Callable[[EngineEvent], Any] | Any] = []

    def subscribe(
        self,
        event_type: EngineEventType,
        handler: Callable[[EngineEvent], Any] | Any,
    ) -> None:
        self._handlers[event_type].append(handler)

    def subscribe_all(
        self,
        handler: Callable[[EngineEvent], Any] | Any,
    ) -> None:
        self._global.append(handler)

    def unsubscribe(
        self,
        event_type: EngineEventType,
        handler: Callable[[EngineEvent], Any] | Any,
    ) -> None:
        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)

    def unsubscribe_all(
        self,
        handler: Callable[[EngineEvent], Any] | Any,
    ) -> None:
        if handler in self._global:
            self._global.remove(handler)

    def publish(
        self,
        event: EngineEvent,
    ) -> None:

        for handler in tuple(self._global):
            self._dispatch(handler, event)

        for handler in tuple(self._handlers[event.type]):
            self._dispatch(handler, event)

    @staticmethod
    def _dispatch(
        handler: Callable[[EngineEvent], Any] | Any,
        event: EngineEvent,
    ) -> None:
        """
        Dispatch to either:

        - Callable(event)
        - Observer.notify(event)
        """

        notify = getattr(handler, "notify", None)

        if callable(notify):
            notify(event)
        else:
            handler(event)

    def clear(self) -> None:
        self._handlers.clear()
        self._global.clear()
