from __future__ import annotations

from abc import ABC, abstractmethod

from platform_core.services.collection import ServiceCollection


class Registrar(ABC):
    """
    Registers one subsystem into the service collection.
    """

    @abstractmethod
    def register(
        self,
        services: ServiceCollection,
    ) -> None: ...
