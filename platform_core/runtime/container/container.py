from __future__ import annotations

from collections.abc import Callable

from .exceptions import (
    ServiceAlreadyRegisteredError,
    ServiceNotRegisteredError,
)
from .interfaces import IServiceContainer
from .lifetime import Lifetime
from .service_descriptor import ServiceDescriptor


class ServiceContainer(IServiceContainer):
    def __init__(self) -> None:
        self._services: dict[type, ServiceDescriptor] = {}

    def register_singleton(
        self,
        interface: type,
        implementation: type | Callable,
    ) -> None:

        if interface in self._services:
            raise ServiceAlreadyRegisteredError(f"{interface.__name__} already registered.")

        self._services[interface] = ServiceDescriptor(
            interface=interface,
            implementation=implementation,
            lifetime=Lifetime.SINGLETON,
        )

    def register_transient(
        self,
        interface: type,
        implementation: type | Callable,
    ) -> None:

        if interface in self._services:
            raise ServiceAlreadyRegisteredError(f"{interface.__name__} already registered.")

        self._services[interface] = ServiceDescriptor(
            interface=interface,
            implementation=implementation,
            lifetime=Lifetime.TRANSIENT,
        )

    def resolve(self, interface: type):

        descriptor = self._services.get(interface)

        if descriptor is None:
            raise ServiceNotRegisteredError(f"{interface.__name__} is not registered.")

        if descriptor.lifetime == Lifetime.SINGLETON:
            if descriptor.instance is None:
                descriptor.instance = descriptor.implementation()

            return descriptor.instance

        return descriptor.implementation()

    def contains(self, interface: type) -> bool:
        return interface in self._services

    def clear(self) -> None:
        self._services.clear()
