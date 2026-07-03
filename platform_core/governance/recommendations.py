"""Recommendation Engine - Generates actionable recommendations from findings."""

from __future__ import annotations

import threading
from typing import Any

from platform_core.governance.types import Finding, FindingSeverity, Recommendation


class RecommendationEngine:
    """Generates prioritized recommendations from findings."""

    SEVERITY_PRIORITY: dict[FindingSeverity, int] = {
        FindingSeverity.CRITICAL: 1,
        FindingSeverity.HIGH: 2,
        FindingSeverity.MEDIUM: 3,
        FindingSeverity.LOW: 4,
        FindingSeverity.INFO: 5,
    }

    EFFORT_ESTIMATES: dict[str, str] = {
        "security": "2-4 hours",
        "testing": "4-8 hours",
        "documentation": "1-2 hours",
        "architecture": "8-16 hours",
        "dependencies": "2-4 hours",
        "ci_cd": "2-4 hours",
        "performance": "4-8 hours",
        "compliance": "4-8 hours",
        "healthcare_standards": "8-16 hours",
    }

    def __init__(self) -> None:
        self._recommendations: dict[str, Recommendation] = {}
        self._lock = threading.RLock()

    def generate_recommendations(
        self,
        findings: list[Finding],
        repository: str = "",
    ) -> list[Recommendation]:
        recommendations: list[Recommendation] = []

        sorted_findings = sorted(
            findings,
            key=lambda f: self.SEVERITY_PRIORITY.get(f.severity, 5),
        )

        for finding in sorted_findings:
            rec = self._finding_to_recommendation(finding, repository)
            recommendations.append(rec)
            with self._lock:
                self._recommendations[rec.id] = rec

        return recommendations

    def _finding_to_recommendation(self, finding: Finding, repository: str) -> Recommendation:
        category = finding.category or "general"
        effort = self.EFFORT_ESTIMATES.get(category, "2-4 hours")

        return Recommendation(
            finding_id=finding.id,
            repository=repository or finding.repository,
            category=category,
            priority=self.SEVERITY_PRIORITY.get(finding.severity, 5),
            title=f"Fix: {finding.title}",
            description=finding.recommendation or finding.description,
            estimated_effort=effort,
            estimated_impact=self._estimate_impact(finding.severity),
            target_version=finding.target_version,
        )

    def _estimate_impact(self, severity: FindingSeverity) -> str:
        impacts = {
            FindingSeverity.CRITICAL: "Blocks release",
            FindingSeverity.HIGH: "Must resolve before release",
            FindingSeverity.MEDIUM: "Should resolve before release",
            FindingSeverity.LOW: "Can defer to next release",
            FindingSeverity.INFO: "No impact on release",
        }
        return impacts.get(severity, "Unknown impact")

    def prioritize(self, recommendations: list[Recommendation]) -> list[Recommendation]:
        return sorted(recommendations, key=lambda r: r.priority)

    def group_by_category(
        self, recommendations: list[Recommendation]
    ) -> dict[str, list[Recommendation]]:
        groups: dict[str, list[Recommendation]] = {}
        for rec in recommendations:
            cat = rec.category or "general"
            groups.setdefault(cat, []).append(rec)
        return groups

    def estimate_total_effort(self, recommendations: list[Recommendation]) -> dict[str, Any]:
        hours_map = {
            "1-2 hours": 2,
            "2-4 hours": 3,
            "4-8 hours": 6,
            "8-16 hours": 12,
        }
        total = 0
        by_category: dict[str, int] = {}
        for rec in recommendations:
            hours = hours_map.get(rec.estimated_effort, 4)
            total += hours
            cat = rec.category or "general"
            by_category[cat] = by_category.get(cat, 0) + hours
        return {"total_hours": total, "by_category": by_category}

    def get_recommendation(self, recommendation_id: str) -> Recommendation | None:
        with self._lock:
            return self._recommendations.get(recommendation_id)

    def count(self) -> int:
        with self._lock:
            return len(self._recommendations)
