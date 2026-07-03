from uuid import uuid4

import pytest

from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.cancellation_coordinator import (
    CancellationCoordinator,
)
from platform_core.engine.context import EngineContext


def make_context() -> EngineContext:

    return EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=CancellationToken(),
    )


def test_not_cancelled() -> None:

    coordinator = CancellationCoordinator()

    ctx = make_context()

    assert coordinator.is_cancelled(ctx) is False


def test_cancelled() -> None:

    coordinator = CancellationCoordinator()

    ctx = make_context()

    ctx.cancellation_token.cancel()

    assert coordinator.is_cancelled(ctx) is True


def test_raise_if_cancelled() -> None:

    coordinator = CancellationCoordinator()

    ctx = make_context()

    ctx.cancellation_token.cancel()

    with pytest.raises(RuntimeError):
        coordinator.raise_if_cancelled(ctx)
