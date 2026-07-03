from uuid import uuid4

from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.errors import EngineErrorCategory
from platform_core.engine.failure_handler import FailureHandler
from platform_core.engine.result import EngineStatus


def make_context() -> EngineContext:

    return EngineContext(
        execution_id=uuid4(),
        execution_mode="normal",
        cancellation_token=CancellationToken(),
    )


def test_failure_handler_returns_failed_result() -> None:

    handler = FailureHandler()

    result = handler.handle(
        make_context(),
        RuntimeError("boom"),
        0.25,
    )

    assert result.status is EngineStatus.FAILED
    assert result.success is False
    assert len(result.errors) == 1
    assert result.errors[0].category is EngineErrorCategory.INTERNAL
    assert result.errors[0].message == "boom"
