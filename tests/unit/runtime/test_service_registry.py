from platform_core.runtime.services import ServiceRegistry


def test_service_registry():

    registry = ServiceRegistry()

    service = object()

    registry.register(
        "logger",
        service,
    )

    assert registry.exists("logger")

    assert registry.get("logger") is service

    assert registry.names() == ["logger"]

    registry.unregister("logger")

    assert registry.exists("logger") is False
