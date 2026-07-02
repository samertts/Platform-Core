from __future__ import annotations

from platform_core.registrars.abc import Registrar
from platform_core.runtime.runtime import Runtime
from platform_core.services.collection import ServiceCollection


class RuntimeRegistrar(Registrar):
    def register(
        self,
        services: ServiceCollection,
    ) -> None:

        services.add_singleton(
            "runtime",
            Runtime,
        )
