from platform_core.workflow.context import WorkflowContext
from platform_core.workflow.result import WorkflowResult
from platform_core.workflow.step import WorkflowStep


class Step(WorkflowStep):
    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:

        context.set("done", True)

        return WorkflowResult.ok()


def test_step() -> None:

    context = WorkflowContext()

    step = Step()

    result = step.execute(context)

    assert result.success

    assert context.get("done")
