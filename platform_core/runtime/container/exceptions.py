"""
Dependency Injection Exceptions
"""


class ContainerError(Exception):
    """Base container exception."""


class ServiceAlreadyRegisteredError(ContainerError):
    """Raised when attempting to register an existing service."""


class ServiceNotRegisteredError(ContainerError):
    """Raised when resolving an unknown service."""
