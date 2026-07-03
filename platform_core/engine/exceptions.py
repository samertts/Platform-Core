from __future__ import annotations


class EngineException(Exception):  # noqa: N818
    """Base Engine exception."""


class LifecycleViolation(EngineException):
    """Raised when an invalid lifecycle transition occurs."""
