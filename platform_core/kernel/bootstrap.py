from __future__ import annotations

from platform_core.events import EventBus
from platform_core.kernel.boot_context import BootContext
from platform_core.registrars import (
    CoreRegistrar,
    DoctorRegistrar,
    RegistrarManager,
    RuntimeRegistrar,
)
from platform_core.services.builder import ContainerBuilder
from platform_core.services.collection import ServiceCollection


class Bootstrap:
    """
    Platform composition root.
    """

    def __init__(self) -> None:

        self._manager = RegistrarManager()

        self._configure()

    def _configure(self) -> None:

        self._manager.add(
            CoreRegistrar(),
        )

        self._manager.add(
            RuntimeRegistrar(),
        )

        self._manager.add(
            DoctorRegistrar(),
        )

    def boot(
        self,
    ) -> BootContext:

        services = ServiceCollection()

        self._manager.register_all(
            services,
        )

        container = ContainerBuilder().build(
            services,
        )

        events = EventBus()

        return BootContext(
            container=container,
            events=events,
        )
