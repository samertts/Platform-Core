from uuid import uuid4

from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.hook_dispatcher import HookDispatcher
from platform_core.engine.pipeline_executor import PipelineExecutor
from platform_core.engine.result import EngineResult, EngineStatus


class FakeEngine:
    def __init__(self):

        self.calls = []

    def before_validate(self, ctx):
        self.calls.append("before_validate")

    def validate(self, ctx):
        self.calls.append("validate")

    def after_validate(self, ctx):
        self.calls.append("after_validate")

    def before_prepare(self, ctx):
        self.calls.append("before_prepare")

    def prepare(self, ctx):
        self.calls.append("prepare")

    def after_prepare(self, ctx):
        self.calls.append("after_prepare")

    def before_execute(self, ctx):
        self.calls.append("before_execute")

    def execute(self, ctx):

        self.calls.append("execute")

        return EngineResult(
            status=EngineStatus.COMPLETED,
        )

    def after_execute(self, ctx, result):
        self.calls.append("after_execute")

    def before_finalize(self, ctx):
        self.calls.append("before_finalize")

    def finalize(self, ctx):
        self.calls.append("finalize")

    def after_finalize(self, ctx):
        self.calls.append("after_finalize")


def make_context():

    return EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=CancellationToken(),
    )


def test_pipeline_executor_order():

    executor = PipelineExecutor(
        HookDispatcher(),
    )

    engine = FakeEngine()

    executor.execute(
        engine,
        make_context(),
    )

    assert engine.calls == [
        "before_validate",
        "validate",
        "after_validate",
        "before_prepare",
        "prepare",
        "after_prepare",
        "before_execute",
        "execute",
        "after_execute",
        "before_finalize",
        "finalize",
        "after_finalize",
    ]
