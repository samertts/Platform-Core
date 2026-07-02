from __future__ import annotations

from collections.abc import Callable

from platform_core.engine.events import EngineEvent


EventHandler = Callable[[EngineEvent], None]


class EventPublisher:
    """
    Very lightweight synchronous event dispatcher.

    BaseEngine owns exactly one publisher.
    """

    def __init__(self) -> None:

        self._handlers: list[EventHandler] = []

    def subscribe(
        self,
        handler: EventHandler,
    ) -> None:

        self._handlers.append(handler)

    def publish(
        self,
        event: EngineEvent,
    ) -> None:

        for handler in tuple(self._handlers):
            handler(event)
