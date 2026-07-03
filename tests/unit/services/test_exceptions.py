from platform_core.services.exceptions import (
    InvalidLifetimeError,
    ScopeRequiredError,
    ServiceAlreadyRegisteredError,
    ServiceError,
    ServiceNotFoundError,
)


def test_inheritance() -> None:

    assert issubclass(ServiceAlreadyRegisteredError, ServiceError)
    assert issubclass(ServiceNotFoundError, ServiceError)
    assert issubclass(InvalidLifetimeError, ServiceError)
    assert issubclass(ScopeRequiredError, ServiceError)


def test_raise() -> None:

    try:
        raise ServiceNotFoundError("missing")
    except ServiceError:
        pass
