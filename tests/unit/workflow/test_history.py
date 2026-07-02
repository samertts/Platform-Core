from platform_core.workflow.history import WorkflowHistory
from platform_core.workflow.result import WorkflowResult


def test_history():

    history = WorkflowHistory()

    history.add(
        WorkflowResult.ok()
    )

    assert len(history) == 1

    history.clear()

    assert len(history) == 0
