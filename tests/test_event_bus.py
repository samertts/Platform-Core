from platform_core.events import Event, EventBus


def test_publish() -> None:

    bus = EventBus()

    result: list[int] = []

    def callback(event: Event) -> None:

        result.append(event.payload["value"])

    bus.subscribe(
        "demo",
        callback,
    )

    bus.publish(
        Event(
            name="demo",
            payload={
                "value": 10,
            },
        )
    )

    assert result == [10]
