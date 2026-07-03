from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class EngineEventType(StrEnum):
    # Lifecycle
    CREATED = "created"
    CONFIGURED = "configured"
    INITIALIZED = "initialized"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DISPOSED = "disposed"

    # Pipeline
    BEFORE_VALIDATE = "before_validate"
    AFTER_VALIDATE = "after_validate"

    BEFORE_PREPARE = "before_prepare"
    AFTER_PREPARE = "after_prepare"

    BEFORE_EXECUTE = "before_execute"
    AFTER_EXECUTE = "after_execute"

    BEFORE_FINALIZE = "before_finalize"
    AFTER_FINALIZE = "after_finalize"

    # Diagnostics
    WARNING = "warning"
    ERROR = "error"
    METRIC = "metric"


@dataclass(frozen=True, slots=True)
class EngineEvent:
    """
    Immutable event emitted by BaseEngine.

    This is the canonical event model for observability.
    """

    type: EngineEventType

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    id: UUID = field(default_factory=uuid4)

    payload: dict[str, Any] = field(default_factory=dict)
