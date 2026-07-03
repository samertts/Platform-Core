from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from platform_core.engine.artifact import Artifact
from platform_core.engine.errors import EngineError
from platform_core.engine.warnings import EngineWarning


class EngineStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class EngineResult:
    """
    Immutable snapshot returned from every Engine execution.
    """

    status: EngineStatus

    duration: float = 0.0

    errors: tuple[EngineError, ...] = ()

    warnings: tuple[EngineWarning, ...] = ()

    artifacts: tuple[Artifact, ...] = ()

    metrics: Mapping[str, int | float] = field(default_factory=dict)

    payload: Any | None = None

    @property
    def success(self) -> bool:
        return self.status is EngineStatus.COMPLETED
