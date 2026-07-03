from typing import Any

from platform_core.engine.event_bus import EventBus
from platform_core.engine.events import EngineEvent, EngineEventType
from platform_core.engine.observer import EngineObserver


class FakeObserver(EngineObserver):
    def __init__(self) -> None:

        self.events: list[EngineEvent] = []

    def notify(self, event: Any) -> None:

        self.events.append(event)


def test_observer_receives_event() -> None:

    bus = EventBus()

    observer = FakeObserver()

    bus.subscribe_all(observer)

    bus.publish(
        EngineEvent(
            type=EngineEventType.RUNNING,
        )
    )

    assert len(observer.events) == 1

    assert observer.events[0].type is EngineEventType.RUNNING
