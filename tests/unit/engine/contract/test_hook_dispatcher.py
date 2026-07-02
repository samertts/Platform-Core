from uuid import uuid4

from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.hook_dispatcher import HookDispatcher
from platform_core.engine.result import EngineResult, EngineStatus


class FakeEngine:
    def __init__(self):

        self.calls = []

    def before_validate(self, ctx):
        self.calls.append("before_validate")

    def after_validate(self, ctx):
        self.calls.append("after_validate")

    def before_prepare(self, ctx):
        self.calls.append("before_prepare")

    def after_prepare(self, ctx):
        self.calls.append("after_prepare")

    def before_execute(self, ctx):
        self.calls.append("before_execute")

    def after_execute(self, ctx, result):
        self.calls.append("after_execute")

    def before_finalize(self, ctx):
        self.calls.append("before_finalize")

    def after_finalize(self, ctx):
        self.calls.append("after_finalize")

    def on_failure(self, ctx, exc):
        self.calls.append("on_failure")


def make_context():

    return EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=CancellationToken(),
    )


def test_dispatch_all_hooks():

    dispatcher = HookDispatcher()

    engine = FakeEngine()

    ctx = make_context()

    result = EngineResult(
        status=EngineStatus.COMPLETED,
    )

    dispatcher.before_validate(engine, ctx)
    dispatcher.after_validate(engine, ctx)

    dispatcher.before_prepare(engine, ctx)
    dispatcher.after_prepare(engine, ctx)

    dispatcher.before_execute(engine, ctx)
    dispatcher.after_execute(engine, ctx, result)

    dispatcher.before_finalize(engine, ctx)
    dispatcher.after_finalize(engine, ctx)

    dispatcher.on_failure(
        engine,
        ctx,
        RuntimeError("boom"),
    )

    assert engine.calls == [
        "before_validate",
        "after_validate",
        "before_prepare",
        "after_prepare",
        "before_execute",
        "after_execute",
        "before_finalize",
        "after_finalize",
        "on_failure",
    ]
