"""Discovery Engine core types - enums, dataclasses, and DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class ScanType(str, Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    ON_DEMAND = "on_demand"


class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


class FindingSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingCategory(str, Enum):
    SECURITY = "security"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    ARCHITECTURE = "architecture"
    DEPENDENCIES = "dependencies"
    CI_CD = "ci_cd"
    CODE_QUALITY = "code_quality"
    DOCKER = "docker"


class HealthRating(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


@dataclass
class LanguageInfo:
    primary: str = ""
    distribution: list[dict[str, Any]] = field(default_factory=list)
    total_files: int = 0
    total_loc: int = 0


@dataclass
class FrameworkInfo:
    name: str = ""
    version: str = ""
    category: str = ""
    confidence: float = 0.0
    frameworks: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ArchitectureInfo:
    pattern: str = ""
    confidence: float = 0.0
    features: list[str] = field(default_factory=list)


@dataclass
class DocumentationInfo:
    score: float = 0.0
    has_readme: bool = False
    readme_quality: float = 0.0
    has_changelog: bool = False
    has_contributing: bool = False
    has_license: bool = False
    has_api_docs: bool = False
    has_architecture_docs: bool = False
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class TestingInfo:
    score: float = 0.0
    test_framework: str = ""
    test_files: int = 0
    has_test_config: bool = False
    coverage_available: bool = False
    coverage_percent: float = 0.0
    test_to_code_ratio: float = 0.0
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SecurityInfo:
    score: float = 1.0
    findings: list[dict[str, Any]] = field(default_factory=list)
    has_security_md: bool = False
    has_gitignore: bool = False
    has_env_example: bool = False
    secret_patterns_found: int = 0


@dataclass
class DependencyInfo:
    score: float = 0.0
    total: int = 0
    direct: int = 0
    transitive: int = 0
    outdated: int = 0
    vulnerable: int = 0
    files_found: list[str] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CIInfo:
    score: float = 0.0
    system: str = ""
    has_ci: bool = False
    stages: list[str] = field(default_factory=list)
    deployment_configured: bool = False
    files_found: list[str] = field(default_factory=list)


@dataclass
class DockerInfo:
    detected: bool = False
    base_image: str = ""
    ports: list[int] = field(default_factory=list)
    multi_stage: bool = False
    has_compose: bool = False
    files_found: list[str] = field(default_factory=list)


@dataclass
class Finding:
    id: str = field(default_factory=lambda: str(uuid4()))
    category: FindingCategory = FindingCategory.CODE_QUALITY
    type: str = ""
    severity: FindingSeverity = FindingSeverity.INFO
    message: str = ""
    file: str = ""
    line: int = 0
    recommendation: str = ""


@dataclass
class ScanResult:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    scan_type: ScanType = ScanType.FULL
    status: ScanStatus = ScanStatus.PENDING
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    duration_seconds: float = 0.0
    root_path: str = ""
    files_scanned: int = 0
    total_files: int = 0
    errors: list[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    id: str = field(default_factory=lambda: str(uuid4()))
    scan_id: str = ""
    repository: str = ""
    language: LanguageInfo = field(default_factory=LanguageInfo)
    framework: FrameworkInfo = field(default_factory=FrameworkInfo)
    architecture: ArchitectureInfo = field(default_factory=ArchitectureInfo)
    documentation: DocumentationInfo = field(default_factory=DocumentationInfo)
    testing: TestingInfo = field(default_factory=TestingInfo)
    security: SecurityInfo = field(default_factory=SecurityInfo)
    dependencies: DependencyInfo = field(default_factory=DependencyInfo)
    ci_cd: CIInfo = field(default_factory=CIInfo)
    docker: DockerInfo = field(default_factory=DockerInfo)
    findings: list[Finding] = field(default_factory=list)
    manifest_present: bool = False
    manifest_valid: bool = False
    manifest_errors: list[str] = field(default_factory=list)


@dataclass
class HealthScore:
    overall: float = 0.0
    documentation: float = 0.0
    testing: float = 0.0
    security: float = 0.0
    architecture: float = 0.0
    dependencies: float = 0.0
    ci_cd: float = 0.0
    code_quality: float = 0.0
    rating: HealthRating = HealthRating.CRITICAL


@dataclass
class DiscoveryResult:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    scan_type: ScanType = ScanType.FULL
    scan: ScanResult = field(default_factory=ScanResult)
    analysis: AnalysisResult = field(default_factory=AnalysisResult)
    health_score: HealthScore = field(default_factory=HealthScore)
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    duration_seconds: float = 0.0
    status: ScanStatus = ScanStatus.PENDING


@dataclass
class EcosystemReport:
    id: str = field(default_factory=lambda: str(uuid4()))
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    total_repositories: int = 0
    scanned_repositories: int = 0
    health_distribution: dict[str, int] = field(default_factory=dict)
    average_health_score: float = 0.0
    top_repositories: list[dict[str, Any]] = field(default_factory=list)
    bottom_repositories: list[dict[str, Any]] = field(default_factory=list)
    findings_summary: dict[str, int] = field(default_factory=dict)
    trends: dict[str, Any] = field(default_factory=dict)


@dataclass
class RepositoryReport:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    health_score: HealthScore = field(default_factory=HealthScore)
    category_scores: dict[str, float] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
