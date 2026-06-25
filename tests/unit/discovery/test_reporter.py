"""Unit tests for Reporter."""

import pytest
from platform_core.discovery.reporter import Reporter
from platform_core.discovery.types import (
    AnalysisResult,
    DiscoveryResult,
    HealthScore,
    HealthRating,
    ScanStatus,
    ScanResult,
    DocumentationInfo,
    TestingInfo,
    SecurityInfo,
    ArchitectureInfo,
    DependencyInfo,
    CIInfo,
    Finding,
    FindingCategory,
    FindingSeverity,
)


class TestReporter:
    def test_init(self) -> None:
        reporter = Reporter()
        assert reporter is not None

    def test_generate_ecosystem_report(self) -> None:
        reporter = Reporter()
        results = [
            DiscoveryResult(
                repository="repo-a",
                status=ScanStatus.SUCCESS,
                health_score=HealthScore(overall=0.8, rating=HealthRating.GOOD),
            ),
            DiscoveryResult(
                repository="repo-b",
                status=ScanStatus.SUCCESS,
                health_score=HealthScore(overall=0.6, rating=HealthRating.FAIR),
            ),
        ]
        report = reporter.generate_ecosystem_report(results)
        assert report.total_repositories == 2
        assert report.scanned_repositories == 2
        assert report.average_health_score > 0

    def test_generate_ecosystem_report_empty(self) -> None:
        reporter = Reporter()
        report = reporter.generate_ecosystem_report([])
        assert report.total_repositories == 0

    def test_generate_repository_report(self) -> None:
        reporter = Reporter()
        result = DiscoveryResult(
            repository="test-repo",
            status=ScanStatus.SUCCESS,
            health_score=HealthScore(overall=0.75, rating=HealthRating.GOOD),
            analysis=AnalysisResult(documentation=DocumentationInfo(has_readme=True)),
        )
        report = reporter.generate_repository_report(result)
        assert report.repository == "test-repo"
        assert report.health_score.overall == 0.75
        assert len(report.recommendations) >= 0

    def test_recommendations_for_missing_readme(self) -> None:
        reporter = Reporter()
        result = DiscoveryResult(
            repository="test",
            status=ScanStatus.SUCCESS,
            health_score=HealthScore(overall=0.3, rating=HealthRating.POOR),
            analysis=AnalysisResult(
                documentation=DocumentationInfo(has_readme=False),
                testing=TestingInfo(test_files=0),
            ),
        )
        report = reporter.generate_repository_report(result)
        assert any("README" in r["message"] for r in report.recommendations)

    def test_recommendations_for_no_tests(self) -> None:
        reporter = Reporter()
        result = DiscoveryResult(
            repository="test",
            status=ScanStatus.SUCCESS,
            health_score=HealthScore(overall=0.3, rating=HealthRating.POOR),
            analysis=AnalysisResult(
                testing=TestingInfo(test_files=0),
            ),
        )
        report = reporter.generate_repository_report(result)
        assert any("test" in r["message"].lower() for r in report.recommendations)

    def test_format_health_summary(self) -> None:
        reporter = Reporter()
        score = HealthScore(
            overall=0.8,
            documentation=0.9,
            testing=0.7,
            security=0.85,
            architecture=0.8,
            dependencies=0.6,
            ci_cd=0.9,
            code_quality=0.7,
            rating=HealthRating.GOOD,
        )
        summary = reporter.format_health_summary(score)
        assert "GOOD" in summary
        assert "80.0%" in summary

    def test_ecosystem_report_distribution(self) -> None:
        reporter = Reporter()
        results = [
            DiscoveryResult(
                repository=f"repo-{i}",
                status=ScanStatus.SUCCESS,
                health_score=HealthScore(
                    overall=score,
                    rating=HealthRating.GOOD if score >= 0.7 else HealthRating.FAIR,
                ),
            )
            for i, score in enumerate([0.9, 0.8, 0.6, 0.5, 0.3])
        ]
        report = reporter.generate_ecosystem_report(results)
        assert "good" in report.health_distribution
        assert "fair" in report.health_distribution
