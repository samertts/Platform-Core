from __future__ import annotations

from enum import StrEnum


class LifecycleState(StrEnum):
    """
    Standard lifecycle states for every Engine.

    See:
        ENGINE_SPEC.md
    """

    CREATED = "created"

    CONFIGURED = "configured"

    INITIALIZED = "initialized"

    READY = "ready"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"

    DISPOSED = "disposed"
