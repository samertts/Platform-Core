from __future__ import annotations

from typing import Any

from platform_core.services.activator import ObjectActivator
from platform_core.services.descriptor import ServiceDescriptor
from platform_core.services.lifetime import ServiceLifetime
from platform_core.services.scope import ServiceScope


class ServiceProvider:
    """
    Responsible only for service lifetimes.

    Object creation is delegated to ObjectActivator.
    """

    def __init__(self) -> None:

        self._singletons: dict[str, Any] = {}

        self._activator = ObjectActivator()

    def create(
        self,
        descriptor: ServiceDescriptor,
        scope: ServiceScope | None = None,
    ) -> Any:

        #
        # Singleton
        #

        if descriptor.lifetime is ServiceLifetime.SINGLETON:
            instance = self._singletons.get(
                descriptor.key,
            )

            if instance is None:
                instance = self._activator.create(
                    descriptor,
                )

                self._singletons[descriptor.key] = instance

            return instance

        #
        # Scoped
        #

        if descriptor.lifetime is ServiceLifetime.SCOPED:
            if scope is None:
                raise RuntimeError("Scoped service requires ServiceScope.")

            if scope.exists(
                descriptor.key,
            ):
                return scope.get(
                    descriptor.key,
                )

            instance = self._activator.create(
                descriptor,
            )

            scope.set(
                descriptor.key,
                instance,
            )

            return instance

        #
        # Transient
        #

        if descriptor.lifetime is ServiceLifetime.TRANSIENT:
            return self._activator.create(
                descriptor,
            )

        raise ValueError(f"Unsupported lifetime: {descriptor.lifetime}")

    def clear(
        self,
    ) -> None:

        self._singletons.clear()
