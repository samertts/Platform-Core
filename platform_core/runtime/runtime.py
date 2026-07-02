from __future__ import annotations

from platform_core.events import Event
from platform_core.events import EventBus
from platform_core.kernel.kernel import Kernel
from platform_core.services.container import ServiceContainer


class Runtime:

    def __init__(
        self,
        container: ServiceContainer,
    ) -> None:

        self.kernel = Kernel(
            container,
        )

        self.events = EventBus()

    def initialize(
        self,
    ) -> None:

        self.kernel.initialize()

        self.events.publish(
            Event(
                name="runtime.initialized",
            )
        )

    def start(
        self,
    ) -> None:

        self.kernel.start()

        self.events.publish(
            Event(
                name="runtime.started",
            )
        )

    def stop(
        self,
    ) -> None:

        self.events.publish(
            Event(
                name="runtime.stopped",
            )
        )

        self.kernel.stop()

    @property
    def running(
        self,
    ) -> bool:

        return self.kernel.lifecycle.running
