from platform_core.workflow.result import WorkflowResult


def test_success():

    result = WorkflowResult.ok(value=1)

    assert result.success

    assert not result.failed

    assert result.data["value"] == 1


def test_failure():

    result = WorkflowResult.error("failed")

    assert result.failed

    assert result.message == "failed"
