from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EngineErrorCategory(str, Enum):
    VALIDATION = "validation"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    EXECUTION = "execution"
    TIMEOUT = "timeout"
    CANCELLATION = "cancellation"
    INTERNAL = "internal"


@dataclass(frozen=True, slots=True)
class EngineError:
    category: EngineErrorCategory
    message: str
    code: str | None = None
    cause: Exception | None = None
