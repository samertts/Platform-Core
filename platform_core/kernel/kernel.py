from __future__ import annotations

from platform_core.kernel.lifecycle import Lifecycle
from platform_core.services.container import ServiceContainer


class Kernel:
    """
    Platform kernel.

    Owns the application lifecycle and the root service container.
    """

    def __init__(
        self,
        container: ServiceContainer,
    ) -> None:

        self._container = container

        self._lifecycle = Lifecycle()

    @property
    def container(
        self,
    ) -> ServiceContainer:

        return self._container

    @property
    def lifecycle(
        self,
    ) -> Lifecycle:

        return self._lifecycle

    def initialize(
        self,
    ) -> None:

        self._lifecycle.initialize()

    def start(
        self,
    ) -> None:

        self._lifecycle.start()

    def stop(
        self,
    ) -> None:

        self._lifecycle.stop()
