import pytest

from platform_core.runtime.container import ServiceContainer
from platform_core.runtime.container.exceptions import (
    ServiceAlreadyRegisteredError,
    ServiceNotRegisteredError,
)


class IService:
    pass


class Service(IService):
    pass


def test_register() -> None:

    container = ServiceContainer()

    container.register_singleton(
        IService,
        Service,
    )

    assert container.contains(IService)


def test_singleton() -> None:

    container = ServiceContainer()

    container.register_singleton(
        IService,
        Service,
    )

    first = container.resolve(IService)

    second = container.resolve(IService)

    assert first is second


def test_transient() -> None:

    container = ServiceContainer()

    container.register_transient(
        IService,
        Service,
    )

    first = container.resolve(IService)

    second = container.resolve(IService)

    assert first is not second


def test_duplicate_registration() -> None:

    container = ServiceContainer()

    container.register_singleton(
        IService,
        Service,
    )

    with pytest.raises(ServiceAlreadyRegisteredError):
        container.register_singleton(
            IService,
            Service,
        )


def test_unknown_service() -> None:

    container = ServiceContainer()

    with pytest.raises(ServiceNotRegisteredError):
        container.resolve(IService)
