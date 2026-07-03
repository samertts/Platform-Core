from platform_core.workflow.status import WorkflowStatus


def test_values() -> None:

    assert WorkflowStatus.PENDING.value == "pending"

    assert WorkflowStatus.RUNNING.value == "running"

    assert WorkflowStatus.COMPLETED.value == "completed"

    assert WorkflowStatus.FAILED.value == "failed"

    assert WorkflowStatus.CANCELLED.value == "cancelled"
