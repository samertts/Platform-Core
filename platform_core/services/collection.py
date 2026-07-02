from __future__ import annotations

from typing import Any

from platform_core.services.descriptor import ServiceDescriptor
from platform_core.services.lifetime import ServiceLifetime


class ServiceCollection:
    """
    Fluent registration builder.

    Produces immutable ServiceDescriptor objects.
    """

    def __init__(self) -> None:

        self._services: list[ServiceDescriptor] = []

    def add_singleton(
        self,
        key: str,
        implementation: type[Any],
    ) -> ServiceCollection:

        self._services.append(
            ServiceDescriptor(
                key=key,
                implementation=implementation,
                lifetime=ServiceLifetime.SINGLETON,
            )
        )

        return self

    def add_scoped(
        self,
        key: str,
        implementation: type[Any],
    ) -> ServiceCollection:

        self._services.append(
            ServiceDescriptor(
                key=key,
                implementation=implementation,
                lifetime=ServiceLifetime.SCOPED,
            )
        )

        return self

    def add_transient(
        self,
        key: str,
        implementation: type[Any],
    ) -> ServiceCollection:

        self._services.append(
            ServiceDescriptor(
                key=key,
                implementation=implementation,
                lifetime=ServiceLifetime.TRANSIENT,
            )
        )

        return self

    @property
    def descriptors(self) -> tuple[ServiceDescriptor, ...]:

        return tuple(self._services)
