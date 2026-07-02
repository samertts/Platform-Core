"""
Engineering Metrics
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Metric:
    name: str

    value: float


class MetricsEngine:
    def health_score(
        self,
        total: int,
        failed: int,
    ) -> float:

        if total == 0:
            return 100.0

        return (total - failed) / total * 100.0
