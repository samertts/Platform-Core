from __future__ import annotations

from platform_core.engine.context import EngineContext
from platform_core.engine.errors import EngineError
from platform_core.engine.errors import EngineErrorCategory
from platform_core.engine.result import EngineResult
from platform_core.engine.result import EngineStatus


class FailureHandler:
    """
    Converts unexpected exceptions into EngineResult objects.

    This is the single failure boundary required by ENGINE_SPEC.
    """

    def handle(
        self,
        context: EngineContext,
        exc: Exception,
        duration: float,
    ) -> EngineResult:

        return EngineResult(
            status=EngineStatus.FAILED,
            duration=duration,
            errors=(
                EngineError(
                    category=EngineErrorCategory.INTERNAL,
                    message=str(exc),
                    cause=exc,
                ),
            ),
        )
