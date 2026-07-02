from __future__ import annotations

from enum import Enum


class ServiceLifetime(str, Enum):
    """
    Supported dependency lifetimes.
    """

    SINGLETON = "singleton"
    SCOPED = "scoped"
    TRANSIENT = "transient"
