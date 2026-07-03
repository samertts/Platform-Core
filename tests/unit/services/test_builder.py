from platform_core.services.builder import ContainerBuilder
from platform_core.services.collection import ServiceCollection


class Logger:
    pass


def test_build() -> None:

    services = ServiceCollection()

    services.add_singleton(
        "logger",
        Logger,
    )

    builder = ContainerBuilder()

    container = builder.build(
        services,
    )

    assert container.exists(
        "logger",
    )

    instance = container.resolve(
        "logger",
    )

    assert isinstance(
        instance,
        Logger,
    )
