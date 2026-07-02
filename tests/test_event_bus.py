from platform_core.events import Event, EventBus


def test_publish():

    bus = EventBus()

    result = []

    def callback(event):

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
