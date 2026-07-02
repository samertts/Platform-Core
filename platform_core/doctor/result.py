from __future__ import annotations

from dataclasses import dataclass, field

from platform_core.engine.result import EngineResult


@dataclass(frozen=True, slots=True)
class DoctorResult:
    engine: EngineResult

    score: float = 0.0

    checks: tuple[str, ...] = ()

    warnings: tuple[str, ...] = ()

    failures: tuple[str, ...] = ()

    metrics: dict[str, int] = field(default_factory=dict)
