from uuid import uuid4

from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.runner import EngineRunner
from platform_core.engine.result import EngineResult
from platform_core.engine.result import EngineStatus
from tests.unit.engine.fakes import FakeEngine


def make_context():

    return EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=CancellationToken(),
    )


def test_runner_executes_engine():

    runner = EngineRunner()

    engine = FakeEngine()

    result = runner.run(
        engine,
        make_context(),
    )

    assert result.status is EngineStatus.COMPLETED

    assert engine.state.name == "DISPOSED"


def test_runner_records_history():

    runner = EngineRunner()

    engine = FakeEngine()

    runner.run(
        engine,
        make_context(),
    )

    assert len(engine.history) >= 6
