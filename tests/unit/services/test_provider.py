from platform_core.services.descriptor import ServiceDescriptor
from platform_core.services.lifetime import ServiceLifetime
from platform_core.services.provider import ServiceProvider
from platform_core.services.scope import ServiceScope


class Logger:
    pass


def test_singleton() -> None:

    provider = ServiceProvider()

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
        lifetime=ServiceLifetime.SINGLETON,
    )

    first = provider.create(descriptor)

    second = provider.create(descriptor)

    assert first is second


def test_transient() -> None:

    provider = ServiceProvider()

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
        lifetime=ServiceLifetime.TRANSIENT,
    )

    first = provider.create(descriptor)

    second = provider.create(descriptor)

    assert first is not second


def test_clear() -> None:

    provider = ServiceProvider()

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
        lifetime=ServiceLifetime.SINGLETON,
    )

    first = provider.create(descriptor)

    provider.clear()

    second = provider.create(descriptor)

    assert first is not second


def test_scoped() -> None:

    provider = ServiceProvider()

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
        lifetime=ServiceLifetime.SCOPED,
    )

    scope = ServiceScope()

    first = provider.create(
        descriptor,
        scope,
    )

    second = provider.create(
        descriptor,
        scope,
    )

    assert first is second


def test_two_scopes() -> None:

    provider = ServiceProvider()

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
        lifetime=ServiceLifetime.SCOPED,
    )

    scope1 = ServiceScope()

    scope2 = ServiceScope()

    first = provider.create(
        descriptor,
        scope1,
    )

    second = provider.create(
        descriptor,
        scope2,
    )

    assert first is not second
