from __future__ import annotations

from uuid import uuid4

from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.lifecycle import LifecycleState
from platform_core.engine.result import EngineStatus
from tests.unit.engine.fakes import FakeEngine


def test_cancel_before_pipeline() -> None:

    token = CancellationToken()

    token.cancel()

    context = EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=token,
    )

    engine = FakeEngine()

    result = engine.run(context)

    assert result.status is EngineStatus.CANCELLED

    assert engine.state is LifecycleState.DISPOSED

    assert engine.calls == []
