from platform_core.workflow.context import WorkflowContext
from platform_core.workflow.engine import WorkflowEngine
from platform_core.workflow.result import WorkflowResult
from platform_core.workflow.step import WorkflowStep


class Step(WorkflowStep):

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:

        context.set("finished", True)

        return WorkflowResult.ok()


def test_engine():

    engine = WorkflowEngine()

    engine.add_step(Step())

    result = engine.run()

    assert result.success

    assert result.data["context"].get("finished")
