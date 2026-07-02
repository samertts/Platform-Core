from __future__ import annotations

from uuid import uuid4

from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.result import EngineStatus
from tests.unit.engine.fakes import FakeEngine


class BrokenEngine(FakeEngine):
    def execute(
        self,
        context,
    ):

        raise RuntimeError("boom")


def make_context():

    return EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=CancellationToken(),
    )


def test_failure_returns_result():

    engine = BrokenEngine()

    result = engine.run(
        make_context(),
    )

    assert result.status is EngineStatus.FAILED

    assert len(result.errors) == 1

    assert result.errors[0].message == "boom"
