from platform_core.workflow.pipeline import WorkflowPipeline
from platform_core.workflow.step import WorkflowStep
from platform_core.workflow.result import WorkflowResult
from platform_core.workflow.context import WorkflowContext


class Step(WorkflowStep):

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:

        return WorkflowResult.ok()


def test_pipeline():

    pipeline = WorkflowPipeline()

    pipeline.add(Step())

    pipeline.add(Step())

    assert len(pipeline) == 2
