"""Unit tests for Governance types."""

from platform_core.governance.types import (
    Approval,
    ApprovalStatus,
    ComplianceCheck,
    ComplianceReport,
    ComplianceStatus,
    ConstitutionReport,
    Decision,
    DecisionType,
    Exception,
    ExceptionType,
    Finding,
    FindingSeverity,
    FindingStatus,
    GovernanceRecord,
    Policy,
    PolicyType,
    QualityGate,
    QualityGateResult,
    Recommendation,
    Review,
    ReviewStatus,
    ReviewType,
    RiskAssessment,
    RiskCategory,
    RiskLevel,
    Waiver,
)


class TestGovernanceTypes:
    def test_review_type(self) -> None:
        assert ReviewType.ARCHITECTURE.value == "architecture"
        assert ReviewType.SECURITY.value == "security"
        assert ReviewType.HEALTHCARE_STANDARDS.value == "healthcare_standards"

    def test_review_status(self) -> None:
        assert ReviewStatus.PENDING.value == "pending"
        assert ReviewStatus.COMPLETED.value == "completed"

    def test_finding_severity(self) -> None:
        assert FindingSeverity.CRITICAL.value == "critical"
        assert FindingSeverity.HIGH.value == "high"

    def test_finding_status(self) -> None:
        assert FindingStatus.OPEN.value == "open"
        assert FindingStatus.RESOLVED.value == "resolved"

    def test_risk_level(self) -> None:
        assert RiskLevel.CRITICAL.value == "critical"
        assert RiskLevel.NEGLIGIBLE.value == "negligible"

    def test_risk_category(self) -> None:
        assert RiskCategory.SECURITY.value == "security"
        assert RiskCategory.HEALTHCARE_COMPLIANCE.value == "healthcare_compliance"

    def test_compliance_status(self) -> None:
        assert ComplianceStatus.COMPLIANT.value == "compliant"
        assert ComplianceStatus.NON_COMPLIANT.value == "non_compliant"

    def test_quality_gate_result(self) -> None:
        assert QualityGateResult.PASSED.value == "passed"
        assert QualityGateResult.FAILED.value == "failed"

    def test_decision_type(self) -> None:
        assert DecisionType.APPROVE.value == "approve"
        assert DecisionType.REJECT.value == "reject"

    def test_exception_type(self) -> None:
        assert ExceptionType.SECURITY.value == "security"
        assert ExceptionType.COMPLIANCE.value == "compliance"

    def test_policy_type(self) -> None:
        assert PolicyType.MANDATORY.value == "mandatory"
        assert PolicyType.RECOMMENDED.value == "recommended"

    def test_review(self) -> None:
        r = Review(repository="test", review_type=ReviewType.ARCHITECTURE)
        assert r.repository == "test"
        assert r.review_type == ReviewType.ARCHITECTURE

    def test_finding(self) -> None:
        f = Finding(severity=FindingSeverity.CRITICAL, title="test")
        assert f.severity == FindingSeverity.CRITICAL
        assert f.title == "test"

    def test_decision(self) -> None:
        d = Decision(decision_type=DecisionType.APPROVE)
        assert d.decision_type == DecisionType.APPROVE

    def test_recommendation(self) -> None:
        r = Recommendation(title="fix this", priority=1)
        assert r.title == "fix this"

    def test_risk_assessment(self) -> None:
        r = RiskAssessment(risk_category=RiskCategory.SECURITY, risk_level=RiskLevel.HIGH)
        assert r.risk_category == RiskCategory.SECURITY

    def test_compliance_check(self) -> None:
        c = ComplianceCheck(standard="constitution", status=ComplianceStatus.COMPLIANT)
        assert c.standard == "constitution"

    def test_quality_gate(self) -> None:
        q = QualityGate(result=QualityGateResult.PASSED)
        assert q.result == QualityGateResult.PASSED

    def test_exception(self) -> None:
        e = Exception(exception_type=ExceptionType.SECURITY, reason="test")
        assert e.exception_type == ExceptionType.SECURITY

    def test_approval(self) -> None:
        a = Approval(status=ApprovalStatus.APPROVED)
        assert a.status == ApprovalStatus.APPROVED

    def test_policy(self) -> None:
        p = Policy(name="test-policy", policy_type=PolicyType.MANDATORY)
        assert p.name == "test-policy"

    def test_waiver(self) -> None:
        w = Waiver(reason="test waiver")
        assert w.reason == "test waiver"

    def test_governance_record(self) -> None:
        r = GovernanceRecord(action="test_action")
        assert r.action == "test_action"

    def test_compliance_report(self) -> None:
        r = ComplianceReport(repository="test", overall_status=ComplianceStatus.COMPLIANT)
        assert r.repository == "test"

    def test_constitution_report(self) -> None:
        r = ConstitutionReport(repository="test", compliant=True, score=0.9)
        assert r.compliant is True
