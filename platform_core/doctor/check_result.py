from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CheckStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


@dataclass(frozen=True, slots=True)
class CheckResult:
    """
    Immutable result produced by a Doctor check.
    """

    id: str
    name: str
    status: CheckStatus

    message: str = ""

    score: int = 0

    duration: float = 0.0

    metadata: dict[str, str] = field(default_factory=dict)
