from __future__ import annotations

from typing import Any

from platform_core.services.descriptor import ServiceDescriptor
from platform_core.services.provider import ServiceProvider
from platform_core.services.registry import ServiceRegistry
from platform_core.services.scope import ServiceScope


class ServiceContainer:
    """
    High-level Dependency Injection container.
    """

    def __init__(self) -> None:

        self._registry = ServiceRegistry()

        self._provider = ServiceProvider()

    @property
    def registry(self) -> ServiceRegistry:

        return self._registry

    def register(
        self,
        descriptor: ServiceDescriptor,
    ) -> None:

        self._registry.register(descriptor)

    def exists(
        self,
        key: str,
    ) -> bool:

        return self._registry.exists(key)

    def create_scope(self) -> ServiceScope:

        return ServiceScope()

    def resolve(
        self,
        key: str,
        scope: ServiceScope | None = None,
    ) -> Any:

        descriptor = self._registry.get(key)

        return self._provider.create(
            descriptor,
            scope,
        )

    def clear(self) -> None:

        self._provider.clear()

        self._registry.clear()

    def __len__(self) -> int:

        return len(self._registry)
