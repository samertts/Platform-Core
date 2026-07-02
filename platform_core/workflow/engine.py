from __future__ import annotations

from platform_core.workflow.context import WorkflowContext
from platform_core.workflow.executor import WorkflowExecutor
from platform_core.workflow.pipeline import WorkflowPipeline
from platform_core.workflow.result import WorkflowResult
from platform_core.workflow.step import WorkflowStep
from platform_core.workflow.validator import WorkflowValidator


class WorkflowEngine:
    def __init__(self) -> None:

        self._pipeline = WorkflowPipeline()

        self._validator = WorkflowValidator()

        self._executor = WorkflowExecutor()

    @property
    def pipeline(self) -> WorkflowPipeline:

        return self._pipeline

    def add_step(
        self,
        step: WorkflowStep,
    ) -> WorkflowEngine:

        self._pipeline.add(step)

        return self

    def run(
        self,
        context: WorkflowContext | None = None,
    ) -> WorkflowResult:

        self._validator.validate(
            self._pipeline,
        )

        return self._executor.execute(
            self._pipeline,
            context,
        )

    def clear(self) -> None:

        self._pipeline.clear()
