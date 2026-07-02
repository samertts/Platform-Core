from __future__ import annotations

from platform_core.engine.base import BaseEngine
from platform_core.engine.context import EngineContext
from platform_core.engine.result import EngineResult
from platform_core.engine.result import EngineStatus


class FakeEngine(BaseEngine):

    def __init__(self):

        super().__init__()

        self.calls = []

    def validate(
        self,
        context: EngineContext,
    ) -> None:

        self.calls.append("validate")

    def prepare(
        self,
        context: EngineContext,
    ) -> None:

        self.calls.append("prepare")

    def execute(
        self,
        context: EngineContext,
    ) -> EngineResult:

        self.calls.append("execute")

        return EngineResult(
            status=EngineStatus.COMPLETED,
        )

    def finalize(
        self,
        context: EngineContext,
    ) -> None:

        self.calls.append("finalize")
