from __future__ import annotations

import time

from platform_core.engine.cancellation_coordinator import (
    CancellationCoordinator,
)
from platform_core.engine.context import EngineContext
from platform_core.engine.failure_handler import FailureHandler
from platform_core.engine.hook_dispatcher import HookDispatcher
from platform_core.engine.pipeline_executor import PipelineExecutor
from platform_core.engine.result import EngineResult
from platform_core.engine.result import EngineStatus


class EngineRunner:
    """
    Executes the complete Engine lifecycle.

    This class owns orchestration only.
    """

    def __init__(
        self,
        *,
        hooks: HookDispatcher | None = None,
        failure_handler: FailureHandler | None = None,
        cancellation: CancellationCoordinator | None = None,
    ) -> None:

        self._hooks = hooks or HookDispatcher()

        self._failure = failure_handler or FailureHandler()

        self._cancellation = (
            cancellation
            or CancellationCoordinator()
        )

        self._pipeline = PipelineExecutor(
            self._hooks,
        )

    def run(
        self,
        engine,
        context: EngineContext,
    ) -> EngineResult:

        started = time.perf_counter()

        try:

            engine.configure()

            engine.initialize()

            engine.ready()

            engine.running()

            self._cancellation.raise_if_cancelled(
                context,
            )

            result = self._pipeline.execute(
                engine,
                context,
            )

            engine.completed()

            return EngineResult(
                status=EngineStatus.COMPLETED,
                duration=time.perf_counter()
                - started,
                artifacts=result.artifacts,
                metrics=result.metrics,
                warnings=result.warnings,
                payload=result.payload,
            )

        except Exception as exc:

            engine.failed()

            self._hooks.on_failure(
                engine,
                context,
                exc,
            )

            return self._failure.handle(
                context=context,
                exc=exc,
                duration=time.perf_counter()
                - started,
            )

        finally:

            engine.dispose()
