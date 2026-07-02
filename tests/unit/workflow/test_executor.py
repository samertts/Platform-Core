from platform_core.workflow.context import WorkflowContext
from platform_core.workflow.executor import WorkflowExecutor
from platform_core.workflow.pipeline import WorkflowPipeline
from platform_core.workflow.result import WorkflowResult
from platform_core.workflow.step import WorkflowStep


class Step(WorkflowStep):
    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:

        context.set("value", 5)

        return WorkflowResult.ok()


def test_executor():

    pipeline = WorkflowPipeline()

    pipeline.add(Step())

    result = WorkflowExecutor().execute(pipeline)

    assert result.success

    assert result.data["context"].get("value") == 5
