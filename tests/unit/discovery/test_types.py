"""Unit tests for Discovery Engine types."""

from platform_core.discovery.types import (
    AnalysisResult,
    ArchitectureInfo,
    CIInfo,
    DependencyInfo,
    DiscoveryResult,
    DockerInfo,
    DocumentationInfo,
    EcosystemReport,
    Finding,
    FindingCategory,
    FindingSeverity,
    FrameworkInfo,
    HealthRating,
    HealthScore,
    LanguageInfo,
    RepositoryReport,
    ScanResult,
    ScanStatus,
    ScanType,
    SecurityInfo,
    TestingInfo,
)


class TestDiscoveryTypes:
    def test_scan_type(self) -> None:
        assert ScanType.FULL.value == "full"
        assert ScanType.INCREMENTAL.value == "incremental"
        assert ScanType.ON_DEMAND.value == "on_demand"

    def test_scan_status(self) -> None:
        assert ScanStatus.PENDING.value == "pending"
        assert ScanStatus.RUNNING.value == "running"
        assert ScanStatus.SUCCESS.value == "success"

    def test_finding_severity(self) -> None:
        assert FindingSeverity.CRITICAL.value == "critical"
        assert FindingSeverity.HIGH.value == "high"

    def test_health_rating(self) -> None:
        assert HealthRating.EXCELLENT.value == "excellent"
        assert HealthRating.CRITICAL.value == "critical"

    def test_language_info(self) -> None:
        info = LanguageInfo(primary="Python", total_files=10)
        assert info.primary == "Python"
        assert info.total_files == 10

    def test_framework_info(self) -> None:
        info = FrameworkInfo(name="FastAPI", category="web")
        assert info.name == "FastAPI"

    def test_architecture_info(self) -> None:
        info = ArchitectureInfo(pattern="microservices", confidence=0.8)
        assert info.pattern == "microservices"

    def test_documentation_info(self) -> None:
        info = DocumentationInfo(score=0.7, has_readme=True)
        assert info.score == 0.7
        assert info.has_readme is True

    def test_testing_info(self) -> None:
        info = TestingInfo(score=0.5, test_files=10)
        assert info.test_files == 10

    def test_security_info(self) -> None:
        info = SecurityInfo(score=0.9, has_gitignore=True)
        assert info.score == 0.9

    def test_dependency_info(self) -> None:
        info = DependencyInfo(total=25, direct=10)
        assert info.total == 25

    def test_ci_info(self) -> None:
        info = CIInfo(system="GitHub Actions", has_ci=True)
        assert info.system == "GitHub Actions"

    def test_docker_info(self) -> None:
        info = DockerInfo(detected=True, base_image="python:3.11")
        assert info.detected is True

    def test_scan_result(self) -> None:
        result = ScanResult(repository="test-repo")
        assert result.repository == "test-repo"
        assert result.status == ScanStatus.PENDING

    def test_analysis_result(self) -> None:
        result = AnalysisResult(repository="test-repo")
        assert result.repository == "test-repo"

    def test_health_score(self) -> None:
        score = HealthScore(overall=0.85, rating=HealthRating.GOOD)
        assert score.overall == 0.85
        assert score.rating == HealthRating.GOOD

    def test_finding(self) -> None:
        finding = Finding(
            category=FindingCategory.SECURITY,
            severity=FindingSeverity.HIGH,
            message="Test finding",
        )
        assert finding.category == FindingCategory.SECURITY
        assert finding.severity == FindingSeverity.HIGH

    def test_discovery_result(self) -> None:
        result = DiscoveryResult(repository="test")
        assert result.repository == "test"

    def test_ecosystem_report(self) -> None:
        report = EcosystemReport(total_repositories=10)
        assert report.total_repositories == 10

    def test_repository_report(self) -> None:
        report = RepositoryReport(repository="test")
        assert report.repository == "test"
