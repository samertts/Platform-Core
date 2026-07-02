from __future__ import annotations

from platform_core.doctor.engine import DoctorEngine
from platform_core.registrars.abc import Registrar
from platform_core.services.collection import ServiceCollection


class DoctorRegistrar(Registrar):
    def register(
        self,
        services: ServiceCollection,
    ) -> None:

        services.add_singleton(
            "doctor",
            DoctorEngine,
        )
