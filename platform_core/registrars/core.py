from __future__ import annotations

from platform_core.registrars.abc import Registrar
from platform_core.services.collection import ServiceCollection


class CoreRegistrar(Registrar):
    def register(
        self,
        services: ServiceCollection,
    ) -> None:

        # Core services only.
        pass
