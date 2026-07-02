from __future__ import annotations

import time
from abc import ABC

from platform_core.engine.abc import Engine
from platform_core.engine.context import EngineContext
from platform_core.engine.errors import EngineError
from platform_core.engine.errors import EngineErrorCategory
from platform_core.engine.lifecycle import LifecycleState
from platform_core.engine.lifecycle_machine import LifecycleMachine
from platform_core.engine.result import EngineResult
from platform_core.engine.result import EngineStatus


class BaseEngine(Engine, ABC):
    """
    Reference implementation of the Engine contract.

    Concrete engines implement only:

        validate()
        prepare()
        execute()
        finalize()

    BaseEngine owns:

    - lifecycle
    - timing
    - failure handling
    - cancellation
    - pipeline orchestration
    """

    def __init__(self) -> None:

        self._lifecycle = LifecycleMachine()

    # ---------------------------------------------------------
    # Read-only state
    # ---------------------------------------------------------

    @property
    def state(self) -> LifecycleState:
        return self._lifecycle.state

    @property
    def history(self) -> tuple[LifecycleState, ...]:
        return self._lifecycle.history

    # ---------------------------------------------------------
    # Lifecycle wrappers
    # ---------------------------------------------------------

    def configure(self) -> None:
        self._lifecycle.configure()

    def initialize(self) -> None:
        self._lifecycle.initialize()

    def ready(self) -> None:
        self._lifecycle.ready()

    def running(self) -> None:
        self._lifecycle.running()

    def completed(self) -> None:
        self._lifecycle.completed()

    def failed(self) -> None:
        self._lifecycle.failed()

    def cancelled(self) -> None:
        self._lifecycle.cancelled()

    def dispose(self) -> None:
        self._lifecycle.disposed()

    # ---------------------------------------------------------
    # Hook defaults
    # ---------------------------------------------------------

    def before_validate(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def after_validate(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def before_prepare(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def after_prepare(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def before_execute(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def after_execute(
        self,
        context: EngineContext,
        result: EngineResult,
    ) -> None:
        pass

    def before_finalize(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def after_finalize(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def on_failure(
        self,
        context: EngineContext,
        exc: Exception,
    ) -> None:
        pass

    # ---------------------------------------------------------
    # Main pipeline
    # ---------------------------------------------------------

    def run(
        self,
        context: EngineContext,
    ) -> EngineResult:

        started = time.perf_counter()

        try:

            self.configure()
            self.initialize()
            self.ready()

            self._lifecycle.running()

            if context.cancellation_token.is_cancelled:

                self._lifecycle.cancelled()

                return EngineResult(
                    status=EngineStatus.CANCELLED,
                    duration=time.perf_counter() - started,
                )

            self.before_validate(context)
            self.validate(context)
            self.after_validate(context)

            self.before_prepare(context)
            self.prepare(context)
            self.after_prepare(context)

            self.before_execute(context)

            result = self.execute(context)

            self.after_execute(context, result)

            self.before_finalize(context)
            self.finalize(context)
            self.after_finalize(context)

            self._lifecycle.completed()

            return EngineResult(
                status=EngineStatus.COMPLETED,
                duration=time.perf_counter() - started,
                artifacts=result.artifacts,
                warnings=result.warnings,
                metrics=result.metrics,
                payload=result.payload,
            )

        except Exception as exc:

            self._lifecycle.failed()

            self.on_failure(context, exc)

            return EngineResult(
                status=EngineStatus.FAILED,
                duration=time.perf_counter() - started,
                errors=(
                    EngineError(
                        category=EngineErrorCategory.INTERNAL,
                        message=str(exc),
                        cause=exc,
                    ),
                ),
            )

        finally:

            self.dispose()
