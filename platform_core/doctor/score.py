from __future__ import annotations

from platform_core.doctor.report import DoctorReport


class ScoreCalculator:
    """
    Calculates normalized Doctor score.
    """

    def calculate(
        self,
        report: DoctorReport,
    ) -> int:

        if report.total == 0:
            return 100

        return max(
            0,
            min(
                100,
                report.score,
            ),
        )
