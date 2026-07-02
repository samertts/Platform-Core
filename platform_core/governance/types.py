"""Governance Engine core types - all enums, dataclasses, and DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class ReviewType(str, Enum):
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    PERFORMANCE = "performance"
    API = "api"
    COMPATIBILITY = "compatibility"
    CERTIFICATION = "certification"
    OPERATIONAL = "operational"
    HEALTHCARE_STANDARDS = "healthcare_standards"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FindingSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingStatus(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    WONT_FIX = "wont_fix"
    DEFERRED = "deferred"


class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class RiskCategory(str, Enum):
    ARCHITECTURE = "architecture"
    OPERATIONAL = "operational"
    SECURITY = "security"
    DEPENDENCY = "dependency"
    SCALABILITY = "scalability"
    HEALTHCARE_COMPLIANCE = "healthcare_compliance"
    GOVERNMENT_READINESS = "government_readiness"


class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN = "unknown"


class QualityGateResult(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    WAIVED = "waived"


class DecisionType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    DEFER = "defer"
    WAIVE = "waive"
    ESCALATE = "escalate"


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ExceptionType(str, Enum):
    SECURITY = "security"
    COMPLIANCE = "compliance"
    QUALITY = "quality"
    CERTIFICATION = "certification"
    DEPENDENCY = "dependency"


class PolicyType(str, Enum):
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


@dataclass
class Review:
    id: str = field(default_factory=lambda: str(uuid4()))
    review_type: ReviewType = ReviewType.ARCHITECTURE
    repository: str = ""
    status: ReviewStatus = ReviewStatus.PENDING
    reviewer: str = ""
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    findings: list[Finding] = field(default_factory=list)
    score: float = 0.0
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Finding:
    id: str = field(default_factory=lambda: str(uuid4()))
    review_id: str = ""
    repository: str = ""
    severity: FindingSeverity = FindingSeverity.INFO
    status: FindingStatus = FindingStatus.OPEN
    category: str = ""
    title: str = ""
    description: str = ""
    root_cause: str = ""
    evidence: str = ""
    recommendation: str = ""
    owner: str = ""
    priority: int = 0
    target_version: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Decision:
    id: str = field(default_factory=lambda: str(uuid4()))
    review_id: str = ""
    repository: str = ""
    decision_type: DecisionType = DecisionType.DEFER
    rationale: str = ""
    decided_by: str = ""
    decided_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Recommendation:
    id: str = field(default_factory=lambda: str(uuid4()))
    finding_id: str = ""
    repository: str = ""
    category: str = ""
    priority: int = 0
    title: str = ""
    description: str = ""
    estimated_effort: str = ""
    estimated_impact: str = ""
    target_version: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskAssessment:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    risk_category: RiskCategory = RiskCategory.ARCHITECTURE
    risk_level: RiskLevel = RiskLevel.LOW
    score: float = 0.0
    description: str = ""
    impact: str = ""
    likelihood: str = ""
    mitigation: str = ""
    assessed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    assessed_by: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceCheck:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    standard: str = ""
    status: ComplianceStatus = ComplianceStatus.UNKNOWN
    score: float = 0.0
    checks_passed: int = 0
    checks_failed: int = 0
    checks_total: int = 0
    details: list[dict[str, Any]] = field(default_factory=list)
    checked_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QualityGate:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    version: str = ""
    result: QualityGateResult = QualityGateResult.BLOCKED
    checks: list[dict[str, Any]] = field(default_factory=list)
    critical_findings: int = 0
    high_findings: int = 0
    coverage_met: bool = False
    security_passed: bool = False
    compatibility_passed: bool = False
    certification_passed: bool = False
    manifest_valid: bool = False
    signature_valid: bool = False
    sbom_valid: bool = False
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Exception:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    exception_type: ExceptionType = ExceptionType.COMPLIANCE
    reason: str = ""
    approved_by: str = ""
    approved_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime | None = None
    finding_ids: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    active: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Approval:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    version: str = ""
    status: ApprovalStatus = ApprovalStatus.PENDING
    approved_by: str = ""
    approved_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime | None = None
    conditions: list[str] = field(default_factory=list)
    review_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Policy:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    policy_type: PolicyType = PolicyType.MANDATORY
    category: str = ""
    rules: list[dict[str, Any]] = field(default_factory=list)
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Waiver:
    id: str = field(default_factory=lambda: str(uuid4()))
    finding_id: str = ""
    repository: str = ""
    reason: str = ""
    waived_by: str = ""
    waived_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime | None = None
    conditions: list[str] = field(default_factory=list)
    active: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GovernanceRecord:
    id: str = field(default_factory=lambda: str(uuid4()))
    record_type: str = ""
    repository: str = ""
    action: str = ""
    actor: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    details: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceReport:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    overall_status: ComplianceStatus = ComplianceStatus.UNKNOWN
    overall_score: float = 0.0
    checks: list[ComplianceCheck] = field(default_factory=list)
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConstitutionReport:
    id: str = field(default_factory=lambda: str(uuid4()))
    repository: str = ""
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    compliant: bool = False
    score: float = 0.0
    articles_checked: int = 0
    articles_passed: int = 0
    violations: list[Finding] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
