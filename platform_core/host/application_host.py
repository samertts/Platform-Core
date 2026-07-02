from __future__ import annotations

from platform_core.kernel.bootstrap import Bootstrap
from platform_core.runtime.context.runtime_context import RuntimeContext
from platform_core.runtime.runtime import Runtime


class ApplicationHost:
    """
    High-level application entry point.
    """

    def __init__(self) -> None:

        self._bootstrap = Bootstrap()

        self._runtime: Runtime | None = None

        self._context: RuntimeContext | None = None

    def boot(self) -> RuntimeContext:

        boot = self._bootstrap.boot()

        self._runtime = Runtime(
            boot.container,
        )

        self._runtime.initialize()

        self._runtime.start()

        self._context = RuntimeContext(
            kernel=self._runtime.kernel,
            container=boot.container,
            events=boot.events,
        )

        return self._context

    @property
    def runtime(self) -> Runtime:

        assert self._runtime is not None

        return self._runtime

    @property
    def context(self) -> RuntimeContext | None:

        return self._context
