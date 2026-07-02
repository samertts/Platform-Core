from __future__ import annotations

from platform_core.registrars.abc import Registrar
from platform_core.services.collection import ServiceCollection


class RegistrarManager:

    def __init__(self) -> None:

        self._registrars: list[Registrar] = []

    def add(
        self,
        registrar: Registrar,
    ) -> None:

        self._registrars.append(
            registrar,
        )

    def register_all(
        self,
        services: ServiceCollection,
    ) -> None:

        for registrar in self._registrars:

            registrar.register(
                services,
            )
