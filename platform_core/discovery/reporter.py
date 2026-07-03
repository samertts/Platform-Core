"""Reporter - Generates discovery reports and notifications."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from platform_core.discovery.types import (
    DiscoveryResult,
    EcosystemReport,
    HealthRating,
    HealthScore,
    RepositoryReport,
    ScanStatus,
)


class Reporter:
    """Generates ecosystem and repository health reports."""

    def generate_ecosystem_report(self, results: list[DiscoveryResult]) -> EcosystemReport:
        report = EcosystemReport(
            generated_at=datetime.now(UTC),
            total_repositories=len(results),
            scanned_repositories=sum(1 for r in results if r.status == ScanStatus.SUCCESS),
        )

        scores = [r.health_score.overall for r in results if r.status == ScanStatus.SUCCESS]
        if scores:
            report.average_health_score = round(sum(scores) / len(scores), 3)

        distribution: dict[str, int] = {
            "excellent": 0,
            "good": 0,
            "fair": 0,
            "poor": 0,
            "critical": 0,
        }
        for r in results:
            if r.status == ScanStatus.SUCCESS:
                rating = r.health_score.rating.value
                distribution[rating] = distribution.get(rating, 0) + 1
        report.health_distribution = distribution

        successful = [r for r in results if r.status == ScanStatus.SUCCESS]
        successful.sort(key=lambda r: r.health_score.overall, reverse=True)

        report.top_repositories = [
            {
                "name": r.repository,
                "score": r.health_score.overall,
                "rating": r.health_score.rating.value,
            }
            for r in successful[:5]
        ]
        report.bottom_repositories = (
            [
                {
                    "name": r.repository,
                    "score": r.health_score.overall,
                    "rating": r.health_score.rating.value,
                }
                for r in successful[-5:]
            ]
            if len(successful) > 5
            else [
                {
                    "name": r.repository,
                    "score": r.health_score.overall,
                    "rating": r.health_score.rating.value,
                }
                for r in successful
            ]
        )

        findings_summary: dict[str, int] = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0,
        }
        for r in results:
            for f in r.analysis.findings:
                sev = f.severity.value if hasattr(f.severity, "value") else f.severity
                findings_summary[sev] = findings_summary.get(sev, 0) + 1
        report.findings_summary = findings_summary

        return report

    def generate_repository_report(self, result: DiscoveryResult) -> RepositoryReport:
        report = RepositoryReport(
            repository=result.repository,
            generated_at=datetime.now(UTC),
            health_score=result.health_score,
            category_scores={
                "documentation": result.health_score.documentation,
                "testing": result.health_score.testing,
                "security": result.health_score.security,
                "architecture": result.health_score.architecture,
                "dependencies": result.health_score.dependencies,
                "ci_cd": result.health_score.ci_cd,
                "code_quality": result.health_score.code_quality,
            },
            findings=result.analysis.findings,
        )

        report.recommendations = self._generate_recommendations(result)

        return report

    def _generate_recommendations(self, result: DiscoveryResult) -> list[dict[str, Any]]:
        recommendations: list[dict[str, Any]] = []
        analysis = result.analysis

        if not analysis.documentation.has_readme:
            recommendations.append(
                {
                    "priority": 1,
                    "category": "documentation",
                    "message": (
                        "Add a README.md with project overview, "
                        "installation, and usage instructions"
                    ),
                    "estimated_effort": "1-2 hours",
                }
            )

        if analysis.testing.test_files == 0:
            recommendations.append(
                {
                    "priority": 1,
                    "category": "testing",
                    "message": "Add test files and configure a test framework",
                    "estimated_effort": "4-8 hours",
                }
            )

        if analysis.security.secret_patterns_found > 0:
            recommendations.append(
                {
                    "priority": 1,
                    "category": "security",
                    "message": "Remove hardcoded secrets and use environment variables",
                    "estimated_effort": "1-2 hours",
                }
            )

        if not analysis.ci_cd.has_ci:
            recommendations.append(
                {
                    "priority": 2,
                    "category": "ci_cd",
                    "message": "Set up CI/CD pipeline for automated testing and deployment",
                    "estimated_effort": "2-4 hours",
                }
            )

        if not analysis.documentation.has_changelog:
            recommendations.append(
                {
                    "priority": 3,
                    "category": "documentation",
                    "message": "Add CHANGELOG.md to track version changes",
                    "estimated_effort": "30 minutes",
                }
            )

        if not analysis.documentation.has_license:
            recommendations.append(
                {
                    "priority": 2,
                    "category": "documentation",
                    "message": "Add a LICENSE file",
                    "estimated_effort": "10 minutes",
                }
            )

        recommendations.sort(key=lambda r: r["priority"])
        return recommendations

    def format_health_summary(self, score: HealthScore) -> str:
        rating_emoji = {
            HealthRating.EXCELLENT: "★★★★★",
            HealthRating.GOOD: "★★★★☆",
            HealthRating.FAIR: "★★★☆☆",
            HealthRating.POOR: "★★☆☆☆",
            HealthRating.CRITICAL: "★☆☆☆☆",
        }
        emoji = rating_emoji.get(score.rating, "☆☆☆☆☆")
        return (
            f"{emoji} {score.rating.value.upper()} ({score.overall:.1%})\n"
            f"  Documentation:  {score.documentation:.1%}\n"
            f"  Testing:        {score.testing:.1%}\n"
            f"  Security:       {score.security:.1%}\n"
            f"  Architecture:   {score.architecture:.1%}\n"
            f"  Dependencies:   {score.dependencies:.1%}\n"
            f"  CI/CD:          {score.ci_cd:.1%}\n"
            f"  Code Quality:   {score.code_quality:.1%}"
        )
