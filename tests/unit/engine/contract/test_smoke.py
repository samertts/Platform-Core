from __future__ import annotations

from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest

from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.lifecycle import LifecycleState
from platform_core.engine.result import EngineResult
from platform_core.engine.result import EngineStatus


def test_lifecycle_contains_all_states():

    expected = {
        "created",
        "configured",
        "initialized",
        "ready",
        "running",
        "completed",
        "failed",
        "cancelled",
        "disposed",
    }

    actual = {
        state.value
        for state in LifecycleState
    }

    assert actual == expected


def test_context_is_immutable():

    context = EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=CancellationToken(),
    )

    with pytest.raises(FrozenInstanceError):
        context.execution_mode = "strict"


def test_result_success():

    result = EngineResult(
        status=EngineStatus.COMPLETED,
    )

    assert result.success is True


def test_result_failure():

    result = EngineResult(
        status=EngineStatus.FAILED,
    )

    assert result.success is False


def test_cancellation_token():

    token = CancellationToken()

    assert token.is_cancelled is False

    token.cancel()

    assert token.is_cancelled is True
