from __future__ import annotations

from platform_core.engine.context import EngineContext


class CancellationCoordinator:
    """
    Coordinates cooperative cancellation checks.

    This class centralizes all cancellation logic so that
    BaseEngine and PipelineExecutor never inspect the token
    directly.
    """

    def is_cancelled(
        self,
        context: EngineContext,
    ) -> bool:
        return context.cancellation_token.is_cancelled

    def raise_if_cancelled(
        self,
        context: EngineContext,
    ) -> None:
        if self.is_cancelled(context):
            raise RuntimeError("Engine execution cancelled.")
