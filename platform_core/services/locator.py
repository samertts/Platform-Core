from __future__ import annotations

from typing import Any

from platform_core.services.container import ServiceContainer
from platform_core.services.scope import ServiceScope


class ServiceLocator:
    """
    Thin facade over ServiceContainer.

    This class MUST NOT be injected into Engines.
    It exists only for bootstrap/testing convenience.
    """

    def __init__(
        self,
        container: ServiceContainer,
    ) -> None:

        self._container = container

    def resolve(
        self,
        key: str,
        scope: ServiceScope | None = None,
    ) -> Any:

        return self._container.resolve(
            key,
            scope,
        )

    def exists(
        self,
        key: str,
    ) -> bool:

        return self._container.exists(key)
