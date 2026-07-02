from platform_core.engine.event_publisher import EventPublisher
from platform_core.engine.events import EngineEvent, EngineEventType


def test_publish():

    publisher = EventPublisher()

    received = []

    publisher.subscribe(received.append)

    publisher.publish(
        EngineEvent(
            type=EngineEventType.CREATED,
        )
    )

    assert len(received) == 1

    assert received[0].type is EngineEventType.CREATED


def test_multiple_subscribers():

    publisher = EventPublisher()

    first = []
    second = []

    publisher.subscribe(first.append)
    publisher.subscribe(second.append)

    event = EngineEvent(
        type=EngineEventType.RUNNING,
    )

    publisher.publish(event)

    assert first[0] is event

    assert second[0] is event


def test_event_is_immutable():

    event = EngineEvent(
        type=EngineEventType.COMPLETED,
    )

    try:
        event.payload = {}

        assert False

    except Exception:
        pass
