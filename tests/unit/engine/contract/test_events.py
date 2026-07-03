from platform_core.engine.event_publisher import EventPublisher
from platform_core.engine.events import EngineEvent, EngineEventType


def test_publish() -> None:

    publisher = EventPublisher()

    received: list[EngineEvent] = []

    publisher.subscribe(received.append)

    publisher.publish(
        EngineEvent(
            type=EngineEventType.CREATED,
        )
    )

    assert len(received) == 1

    assert received[0].type is EngineEventType.CREATED


def test_multiple_subscribers() -> None:

    publisher = EventPublisher()

    first: list[EngineEvent] = []
    second: list[EngineEvent] = []

    publisher.subscribe(first.append)
    publisher.subscribe(second.append)

    event = EngineEvent(
        type=EngineEventType.RUNNING,
    )

    publisher.publish(event)

    assert first[0] is event

    assert second[0] is event


def test_event_is_immutable() -> None:

    event = EngineEvent(
        type=EngineEventType.COMPLETED,
    )

    try:
        setattr(event, "payload", {})

        assert False

    except Exception:
        pass
