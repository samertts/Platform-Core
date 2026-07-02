from platform_core.engine.event_bus import EventBus
from platform_core.engine.events import EngineEvent
from platform_core.engine.events import EngineEventType
from platform_core.engine.observer import EngineObserver


class FakeObserver(EngineObserver):

    def __init__(self):

        self.events = []

    def notify(self, event):

        self.events.append(event)


def test_observer_receives_event():

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
