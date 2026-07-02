from platform_core.workflow.context import WorkflowContext


def test_context():

    context = WorkflowContext()

    context.set("x", 10)

    assert context.exists("x")

    assert context.get("x") == 10


def test_clear():

    context = WorkflowContext()

    context.set("a", 1)

    context.clear()

    assert not context.exists("a")
