from __future__ import annotations

from enum import StrEnum


class ServiceLifetime(StrEnum):
    """
    Supported dependency lifetimes.
    """

    SINGLETON = "singleton"
    SCOPED = "scoped"
    TRANSIENT = "transient"
