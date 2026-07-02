from __future__ import annotations


class ServiceError(Exception):
    """Base class for all service-related errors."""


class ServiceAlreadyRegisteredError(ServiceError):
    """Raised when a duplicate service is registered."""


class ServiceNotFoundError(ServiceError):
    """Raised when resolving an unknown service."""


class InvalidLifetimeError(ServiceError):
    """Raised when an unsupported lifetime is encountered."""


class ScopeRequiredError(ServiceError):
    """Raised when a scoped service is resolved without a scope."""
