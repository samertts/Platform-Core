from __future__ import annotations

from platform_core.workflow.context import WorkflowContext
from platform_core.workflow.pipeline import WorkflowPipeline
from platform_core.workflow.result import WorkflowResult


class WorkflowExecutor:
    """
    Executes a workflow pipeline.
    """

    def execute(
        self,
        pipeline: WorkflowPipeline,
        context: WorkflowContext | None = None,
    ) -> WorkflowResult:

        if context is None:
            context = WorkflowContext()

        for step in pipeline:

            result = step.execute(
                context,
            )

            if result.failed:
                return result

        return WorkflowResult.ok(
            context=context,
        )
