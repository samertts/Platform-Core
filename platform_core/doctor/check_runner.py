from __future__ import annotations

import time

from platform_core.doctor.check import DoctorCheck
from platform_core.doctor.check_registry import CheckRegistry
from platform_core.doctor.report import DoctorReport


class CheckRunner:
    """
    Executes all registered Doctor checks.
    """

    def __init__(
        self,
        registry: CheckRegistry,
    ) -> None:

        self._registry = registry

    def run(self) -> DoctorReport:

        started = time.perf_counter()

        checks = []

        score = 0

        for check in self._registry:

            result = check.run()

            checks.append(result)

            score += result.score

        duration = time.perf_counter() - started

        return DoctorReport(
            checks=tuple(checks),
            score=score,
            duration=duration,
        )
