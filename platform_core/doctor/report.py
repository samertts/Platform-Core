from __future__ import annotations

from dataclasses import dataclass, field

from platform_core.doctor.check_result import CheckResult


@dataclass(frozen=True, slots=True)
class DoctorReport:
    """
    Immutable report returned by DoctorEngine.
    """

    checks: tuple[CheckResult, ...] = ()

    score: int = 0

    duration: float = 0.0

    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def passed(self) -> int:
        return sum(c.status.value == "passed" for c in self.checks)

    @property
    def failed(self) -> int:
        return sum(c.status.value == "failed" for c in self.checks)

    @property
    def warnings(self) -> int:
        return sum(c.status.value == "warning" for c in self.checks)

    @property
    def skipped(self) -> int:
        return sum(c.status.value == "skipped" for c in self.checks)

    @property
    def total(self) -> int:
        return len(self.checks)
