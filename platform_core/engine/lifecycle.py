from __future__ import annotations

from enum import Enum


class LifecycleState(str, Enum):
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
