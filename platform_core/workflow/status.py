from __future__ import annotations

from enum import StrEnum


class WorkflowStatus(StrEnum):
    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"
