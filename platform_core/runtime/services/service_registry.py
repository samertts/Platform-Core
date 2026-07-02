from __future__ import annotations

from typing import Any


class ServiceRegistry:
    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(
        self,
        name: str,
        service: Any,
    ) -> None:

        self._services[name] = service

    def unregister(
        self,
        name: str,
    ) -> None:

        self._services.pop(name, None)

    def get(
        self,
        name: str,
    ) -> Any:

        return self._services.get(name)

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._services

    def names(
        self,
    ) -> list[str]:

        return sorted(self._services.keys())

    def clear(self) -> None:

        self._services.clear()
