import pytest

from platform_core.services.descriptor import ServiceDescriptor
from platform_core.services.registry import ServiceRegistry


class Logger:
    pass


class Database:
    pass


def test_register():

    registry = ServiceRegistry()

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
    )

    registry.register(descriptor)

    assert registry.exists("logger")


def test_get():

    registry = ServiceRegistry()

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
    )

    registry.register(descriptor)

    assert registry.get("logger") == descriptor


def test_duplicate():

    registry = ServiceRegistry()

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
    )

    registry.register(descriptor)

    with pytest.raises(ValueError):
        registry.register(descriptor)


def test_unregister():

    registry = ServiceRegistry()

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
    )

    registry.register(descriptor)

    registry.unregister("logger")

    assert not registry.exists("logger")


def test_clear():

    registry = ServiceRegistry()

    registry.register(
        ServiceDescriptor(
            key="logger",
            implementation=Logger,
        )
    )

    registry.register(
        ServiceDescriptor(
            key="database",
            implementation=Database,
        )
    )

    registry.clear()

    assert len(registry) == 0


def test_unknown():

    registry = ServiceRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")
