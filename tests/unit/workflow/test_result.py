from platform_core.workflow.result import WorkflowResult


def test_success() -> None:

    result = WorkflowResult.ok(value=1)

    assert result.success

    assert not result.failed

    assert result.data["value"] == 1


def test_failure() -> None:

    result = WorkflowResult.error("failed")

    assert result.failed

    assert result.message == "failed"
