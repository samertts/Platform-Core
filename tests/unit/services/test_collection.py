from platform_core.services.collection import ServiceCollection
from platform_core.services.lifetime import ServiceLifetime


class Logger:
    pass


class Database:
    pass


class Cache:
    pass


def test_add_singleton() -> None:

    services = ServiceCollection()

    services.add_singleton(
        "logger",
        Logger,
    )

    descriptor = services.descriptors[0]

    assert descriptor.key == "logger"

    assert descriptor.lifetime is ServiceLifetime.SINGLETON


def test_add_scoped() -> None:

    services = ServiceCollection()

    services.add_scoped(
        "database",
        Database,
    )

    descriptor = services.descriptors[0]

    assert descriptor.lifetime is ServiceLifetime.SCOPED


def test_add_transient() -> None:

    services = ServiceCollection()

    services.add_transient(
        "cache",
        Cache,
    )

    descriptor = services.descriptors[0]

    assert descriptor.lifetime is ServiceLifetime.TRANSIENT


def test_multiple() -> None:

    services = ServiceCollection()

    services.add_singleton(
        "logger",
        Logger,
    )

    services.add_scoped(
        "database",
        Database,
    )

    services.add_transient(
        "cache",
        Cache,
    )

    assert len(services.descriptors) == 3
