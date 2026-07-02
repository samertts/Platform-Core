"""Health Scorer - Calculates repository health scores based on analyzer outputs."""

from __future__ import annotations

from platform_core.discovery.types import (AnalysisResult, HealthRating,
                                           HealthScore)


class HealthScorer:
    """Calculates weighted health scores from analysis results."""

    CATEGORY_WEIGHTS: dict[str, float] = {
        "documentation": 0.15,
        "testing": 0.20,
        "security": 0.25,
        "architecture": 0.15,
        "dependencies": 0.10,
        "ci_cd": 0.10,
        "code_quality": 0.05,
    }

    RATING_THRESHOLDS: list[tuple[float, HealthRating]] = [
        (0.9, HealthRating.EXCELLENT),
        (0.7, HealthRating.GOOD),
        (0.5, HealthRating.FAIR),
        (0.3, HealthRating.POOR),
        (0.0, HealthRating.CRITICAL),
    ]

    def __init__(self, custom_weights: dict[str, float] | None = None) -> None:
        self._weights = custom_weights or self.CATEGORY_WEIGHTS.copy()

    def calculate(self, analysis: AnalysisResult) -> HealthScore:
        category_scores = {
            "documentation": analysis.documentation.score,
            "testing": analysis.testing.score,
            "security": analysis.security.score,
            "architecture": analysis.architecture.confidence,
            "dependencies": analysis.dependencies.score,
            "ci_cd": analysis.ci_cd.score,
            "code_quality": self._calculate_code_quality(analysis),
        }

        overall = sum(
            category_scores.get(cat, 0.0) * weight
            for cat, weight in self._weights.items()
        )

        overall = round(min(max(overall, 0.0), 1.0), 3)
        rating = self._get_rating(overall)

        return HealthScore(
            overall=overall,
            documentation=round(category_scores["documentation"], 3),
            testing=round(category_scores["testing"], 3),
            security=round(category_scores["security"], 3),
            architecture=round(category_scores["architecture"], 3),
            dependencies=round(category_scores["dependencies"], 3),
            ci_cd=round(category_scores["ci_cd"], 3),
            code_quality=round(category_scores["code_quality"], 3),
            rating=rating,
        )

    def _calculate_code_quality(self, analysis: AnalysisResult) -> float:
        score = 0.0

        if analysis.language.primary and analysis.language.primary != "Unknown":
            score += 0.3

        if analysis.framework.name:
            score += 0.2

        if analysis.architecture.pattern and analysis.architecture.pattern != "unknown":
            score += 0.2

        if analysis.documentation.has_readme:
            score += 0.15

        if analysis.testing.test_files > 0:
            score += 0.15

        return round(min(score, 1.0), 3)

    def _get_rating(self, score: float) -> HealthRating:
        for threshold, rating in self.RATING_THRESHOLDS:
            if score >= threshold:
                return rating
        return HealthRating.CRITICAL

    def get_category_breakdown(
        self, analysis: AnalysisResult
    ) -> dict[str, dict[str, float]]:
        return {
            "documentation": {
                "score": analysis.documentation.score,
                "weight": self._weights.get("documentation", 0),
                "weighted": analysis.documentation.score
                * self._weights.get("documentation", 0),
            },
            "testing": {
                "score": analysis.testing.score,
                "weight": self._weights.get("testing", 0),
                "weighted": analysis.testing.score * self._weights.get("testing", 0),
            },
            "security": {
                "score": analysis.security.score,
                "weight": self._weights.get("security", 0),
                "weighted": analysis.security.score * self._weights.get("security", 0),
            },
            "architecture": {
                "score": analysis.architecture.confidence,
                "weight": self._weights.get("architecture", 0),
                "weighted": analysis.architecture.confidence
                * self._weights.get("architecture", 0),
            },
            "dependencies": {
                "score": analysis.dependencies.score,
                "weight": self._weights.get("dependencies", 0),
                "weighted": analysis.dependencies.score
                * self._weights.get("dependencies", 0),
            },
            "ci_cd": {
                "score": analysis.ci_cd.score,
                "weight": self._weights.get("ci_cd", 0),
                "weighted": analysis.ci_cd.score * self._weights.get("ci_cd", 0),
            },
        }

    def compare_scores(
        self, current: HealthScore, previous: HealthScore
    ) -> dict[str, Any]:
        return {
            "overall_change": round(current.overall - previous.overall, 3),
            "improved": current.overall > previous.overall,
            "category_changes": {
                "documentation": round(
                    current.documentation - previous.documentation, 3
                ),
                "testing": round(current.testing - previous.testing, 3),
                "security": round(current.security - previous.security, 3),
                "architecture": round(current.architecture - previous.architecture, 3),
                "dependencies": round(current.dependencies - previous.dependencies, 3),
                "ci_cd": round(current.ci_cd - previous.ci_cd, 3),
            },
        }


from typing import Any
