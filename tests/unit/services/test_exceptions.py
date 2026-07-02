from platform_core.services.exceptions import (
    InvalidLifetimeError,
    ScopeRequiredError,
    ServiceAlreadyRegisteredError,
    ServiceError,
    ServiceNotFoundError,
)


def test_inheritance():

    assert issubclass(ServiceAlreadyRegisteredError, ServiceError)
    assert issubclass(ServiceNotFoundError, ServiceError)
    assert issubclass(InvalidLifetimeError, ServiceError)
    assert issubclass(ScopeRequiredError, ServiceError)


def test_raise():

    try:
        raise ServiceNotFoundError("missing")
    except ServiceError:
        pass
