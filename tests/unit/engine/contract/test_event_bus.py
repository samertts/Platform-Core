from platform_core.engine.event_bus import EventBus
from platform_core.engine.events import EngineEvent
from platform_core.engine.events import EngineEventType


def test_subscribe_specific():

    bus = EventBus()

    received = []

    bus.subscribe(
        EngineEventType.CREATED,
        received.append,
    )

    bus.publish(
        EngineEvent(
            type=EngineEventType.CREATED,
        )
    )

    assert len(received) == 1


def test_subscribe_all():

    bus = EventBus()

    received = []

    bus.subscribe_all(received.append)

    bus.publish(
        EngineEvent(
            type=EngineEventType.CREATED,
        )
    )

    bus.publish(
        EngineEvent(
            type=EngineEventType.RUNNING,
        )
    )

    bus.publish(
        EngineEvent(
            type=EngineEventType.COMPLETED,
        )
    )

    assert len(received) == 3


def test_specific_not_called():

    bus = EventBus()

    received = []

    bus.subscribe(
        EngineEventType.FAILED,
        received.append,
    )

    bus.publish(
        EngineEvent(
            type=EngineEventType.CREATED,
        )
    )

    assert received == []
