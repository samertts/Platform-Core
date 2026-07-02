from __future__ import annotations

from platform_core.services.descriptor import ServiceDescriptor


class ServiceRegistry:
    """
    Immutable registry metadata.

    Stores service descriptors only.
    Does NOT instantiate services.
    """

    def __init__(self) -> None:

        self._services: dict[str, ServiceDescriptor] = {}

    def register(
        self,
        descriptor: ServiceDescriptor,
    ) -> None:

        if descriptor.key in self._services:
            raise ValueError(f"Service already registered: {descriptor.key}")

        self._services[descriptor.key] = descriptor

    def unregister(
        self,
        key: str,
    ) -> None:

        self._services.pop(key, None)

    def clear(self) -> None:

        self._services.clear()

    def exists(
        self,
        key: str,
    ) -> bool:

        return key in self._services

    def get(
        self,
        key: str,
    ) -> ServiceDescriptor:

        try:
            return self._services[key]

        except KeyError as exc:
            raise KeyError(f"Unknown service: {key}") from exc

    def all(self) -> tuple[ServiceDescriptor, ...]:

        return tuple(self._services.values())

    def __len__(self) -> int:

        return len(self._services)
