from uuid import uuid4

from platform_core.engine.base import BaseEngine
from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.result import EngineResult, EngineStatus


class HookEngine(BaseEngine):
    def __init__(self):

        super().__init__()

        self.calls = []

    def before_validate(self, context):

        self.calls.append("before_validate")

    def validate(self, context):

        self.calls.append("validate")

    def after_validate(self, context):

        self.calls.append("after_validate")

    def prepare(self, context):

        pass

    def execute(self, context):

        return EngineResult(
            status=EngineStatus.COMPLETED,
        )

    def finalize(self, context):

        pass


def test_validate_hooks():

    engine = HookEngine()

    ctx = EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=CancellationToken(),
    )

    engine.run(ctx)

    assert engine.calls == [
        "before_validate",
        "validate",
        "after_validate",
    ]
