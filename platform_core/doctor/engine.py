from __future__ import annotations

from platform_core.doctor.check_registry import CheckRegistry
from platform_core.doctor.check_runner import CheckRunner
from platform_core.engine.base import BaseEngine
from platform_core.engine.context import EngineContext
from platform_core.engine.result import EngineResult, EngineStatus


class DoctorEngine(BaseEngine):
    """
    Production Doctor Engine.
    """

    def __init__(
        self,
        registry: CheckRegistry,
    ) -> None:

        super().__init__()

        self._registry = registry

    def validate(
        self,
        context: EngineContext,
    ) -> None:
        return None

    def prepare(
        self,
        context: EngineContext,
    ) -> None:
        return None

    def execute(
        self,
        context: EngineContext,
    ) -> EngineResult:

        report = CheckRunner(self._registry).run()

        return EngineResult(
            status=EngineStatus.COMPLETED,
            payload=report,
            metrics={
                "checks": report.total,
                "score": report.score,
            },
        )

    def finalize(
        self,
        context: EngineContext,
    ) -> None:
        return None
