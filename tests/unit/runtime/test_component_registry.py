from platform_core.kernel.registry import ComponentRegistry


def test_registry():

    registry = ComponentRegistry()

    service = object()

    registry.register(
        "runtime",
        service,
    )

    assert registry.exists("runtime")

    assert registry.get("runtime") is service

    registry.unregister("runtime")

    assert registry.exists("runtime") is False
