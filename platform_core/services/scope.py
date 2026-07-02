from __future__ import annotations

from typing import Any


class ServiceScope:
    """
    Stores scoped service instances.

    A new scope is created for each logical operation
    (request, command, workflow, etc.).
    """

    def __init__(self) -> None:

        self._instances: dict[str, Any] = {}

    def exists(
        self,
        key: str,
    ) -> bool:

        return key in self._instances

    def get(
        self,
        key: str,
    ) -> Any:

        return self._instances[key]

    def set(
        self,
        key: str,
        instance: Any,
    ) -> None:

        self._instances[key] = instance

    def clear(self) -> None:

        self._instances.clear()

    def __len__(self) -> int:

        return len(self._instances)
