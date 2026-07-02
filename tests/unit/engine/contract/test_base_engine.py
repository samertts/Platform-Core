from __future__ import annotations

from uuid import uuid4

from tests.unit.engine.fakes import FakeEngine

from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.lifecycle import LifecycleState
from platform_core.engine.result import EngineStatus


def make_context() -> EngineContext:
    return EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=CancellationToken(),
    )


def test_run_pipeline():

    engine = FakeEngine()

    result = engine.run(make_context())

    assert result.status is EngineStatus.COMPLETED

    assert engine.calls == [
        "validate",
        "prepare",
        "execute",
        "finalize",
    ]


def test_engine_disposed_after_run():

    engine = FakeEngine()

    engine.run(make_context())

    assert engine.state is LifecycleState.DISPOSED


def test_duration_recorded():

    engine = FakeEngine()

    result = engine.run(make_context())

    assert result.duration >= 0


def test_history_is_recorded():

    engine = FakeEngine()

    engine.run(make_context())

    assert engine.history == (
        LifecycleState.CREATED,
        LifecycleState.CONFIGURED,
        LifecycleState.INITIALIZED,
        LifecycleState.READY,
        LifecycleState.RUNNING,
        LifecycleState.COMPLETED,
        LifecycleState.DISPOSED,
    )
