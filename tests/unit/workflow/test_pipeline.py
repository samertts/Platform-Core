from platform_core.workflow.context import WorkflowContext
from platform_core.workflow.pipeline import WorkflowPipeline
from platform_core.workflow.result import WorkflowResult
from platform_core.workflow.step import WorkflowStep


class Step(WorkflowStep):
    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:

        return WorkflowResult.ok()


def test_pipeline() -> None:

    pipeline = WorkflowPipeline()

    pipeline.add(Step())

    pipeline.add(Step())

    assert len(pipeline) == 2
