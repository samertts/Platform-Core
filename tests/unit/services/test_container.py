from platform_core.services.container import ServiceContainer
from platform_core.services.descriptor import ServiceDescriptor
from platform_core.services.lifetime import ServiceLifetime
from platform_core.services.scope import ServiceScope


class Logger:
    pass


def test_register() -> None:

    container = ServiceContainer()

    container.register(
        ServiceDescriptor(
            key="logger",
            implementation=Logger,
        )
    )

    assert container.exists("logger")


def test_resolve_singleton() -> None:

    container = ServiceContainer()

    container.register(
        ServiceDescriptor(
            key="logger",
            implementation=Logger,
            lifetime=ServiceLifetime.SINGLETON,
        )
    )

    first = container.resolve("logger")
    second = container.resolve("logger")

    assert first is second


def test_resolve_transient() -> None:

    container = ServiceContainer()

    container.register(
        ServiceDescriptor(
            key="logger",
            implementation=Logger,
            lifetime=ServiceLifetime.TRANSIENT,
        )
    )

    first = container.resolve("logger")
    second = container.resolve("logger")

    assert first is not second


def test_clear() -> None:

    container = ServiceContainer()

    container.register(
        ServiceDescriptor(
            key="logger",
            implementation=Logger,
        )
    )

    container.clear()

    assert len(container) == 0


def test_create_scope() -> None:

    container = ServiceContainer()

    scope = container.create_scope()

    assert isinstance(scope, ServiceScope)


def test_resolve_scoped() -> None:

    container = ServiceContainer()

    container.register(
        ServiceDescriptor(
            key="logger",
            implementation=Logger,
            lifetime=ServiceLifetime.SCOPED,
        )
    )

    scope = container.create_scope()

    first = container.resolve(
        "logger",
        scope,
    )

    second = container.resolve(
        "logger",
        scope,
    )

    assert first is second
