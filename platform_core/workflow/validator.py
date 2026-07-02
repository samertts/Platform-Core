from __future__ import annotations

from platform_core.workflow.pipeline import WorkflowPipeline


class WorkflowValidator:
    def validate(
        self,
        pipeline: WorkflowPipeline,
    ) -> None:

        if len(pipeline) == 0:
            raise ValueError("Workflow pipeline is empty.")
