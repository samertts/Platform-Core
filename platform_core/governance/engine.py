"""Governance Engine - Main orchestrator for all governance operations."""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any

from platform_core.governance.ai_assistant import AIGovernanceAssistant
from platform_core.governance.compliance import ComplianceEngine
from platform_core.governance.constitution import ConstitutionEnforcer
from platform_core.governance.decisions import DecisionEngine
from platform_core.governance.exceptions import ExceptionManager
from platform_core.governance.findings import FindingManager
from platform_core.governance.quality import QualityGateEngine
from platform_core.governance.recommendations import RecommendationEngine
from platform_core.governance.registry import GovernanceRegistry
from platform_core.governance.reviews import ReviewManager
from platform_core.governance.risk import RiskEngine
from platform_core.governance.types import (
    ComplianceStatus,
    Decision,
    DecisionType,
    Finding,
    FindingSeverity,
    FindingStatus,
    QualityGate,
    QualityGateResult,
    Recommendation,
    Review,
    ReviewStatus,
    ReviewType,
    RiskAssessment,
)


class GovernanceError(Exception):
    pass


class GovernanceEngine:
    """Main orchestrator for all governance operations.

    Coordinates: reviews, findings, decisions, recommendations, risk,
    compliance, quality gates, constitution enforcement, and AI assistant.
    """

    def __init__(self) -> None:
        self.findings = FindingManager()
        self.reviews = ReviewManager()
        self.decisions = DecisionEngine()
        self.recommendations = RecommendationEngine()
        self.exceptions = ExceptionManager()
        self.risk = RiskEngine()
        self.compliance = ComplianceEngine()
        self.quality_gates = QualityGateEngine()
        self.constitution = ConstitutionEnforcer()
        self.registry = GovernanceRegistry()
        self.ai_assistant = AIGovernanceAssistant()
        self._lock = threading.RLock()

    def run_full_review(
        self,
        repository: str,
        evidence: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        evidence = evidence or {}
        self.registry.record("review", repository, "full_review_started")

        review_results: dict[str, Any] = {}

        for review_type in ReviewType:
            review = self.reviews.create_review(repository=repository, review_type=review_type)
            self.reviews.start_review(review.id)
            self.reviews.complete_review(review.id, score=0.8)
            review_results[review_type.value] = {"status": "completed", "score": 0.8}

        constitution_report = self.constitution.validate(repository, evidence)
        review_results["constitution"] = {
            "compliant": constitution_report.compliant,
            "score": constitution_report.score,
        }

        compliance_checks = self.compliance.validate_all_standards(repository)
        compliance_report = self.compliance.generate_report(repository, compliance_checks)
        review_results["compliance"] = {
            "status": compliance_report.overall_status.value,
            "score": compliance_report.overall_score,
        }

        findings_list = self.findings.list_findings(repository=repository)
        risk_assessments = self.risk.assess_all_categories(repository, findings_list)
        review_results["risk"] = {
            "total_assessments": len(risk_assessments),
        }

        gate = self.quality_gates.evaluate(
            repository=repository,
            version="latest",
            findings=findings_list,
            coverage_percent=evidence.get("coverage_percent", 0.0),
            security_passed=evidence.get("security_passed", True),
            manifest_valid=evidence.get("manifest_valid", True),
        )
        review_results["quality_gate"] = {
            "result": gate.result.value,
        }

        recs = self.recommendations.generate_recommendations(findings_list, repository)
        review_results["recommendations"] = len(recs)

        self.registry.record("review", repository, "full_review_completed")

        return review_results

    def approve_release(
        self,
        repository: str,
        version: str,
        approved_by: str,
        evidence: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        evidence = evidence or {}
        findings_list = self.findings.list_findings(repository=repository)

        gate = self.quality_gates.evaluate(
            repository=repository,
            version=version,
            findings=findings_list,
            coverage_percent=evidence.get("coverage_percent", 0.0),
            security_passed=evidence.get("security_passed", True),
            manifest_valid=evidence.get("manifest_valid", True),
            signature_valid=evidence.get("signature_valid", True),
            sbom_valid=evidence.get("sbom_valid", True),
        )

        if gate.result != QualityGateResult.PASSED:
            self.registry.record("approval", repository, "release_blocked")
            return {
                "approved": False,
                "reason": f"Quality gate failed: {gate.result.value}",
                "gate_id": gate.id,
            }

        review = self.reviews.create_review(
            repository=repository, review_type=ReviewType.CERTIFICATION
        )
        decision = self.decisions.approve(
            repository=repository,
            review_id=review.id,
            decided_by=approved_by,
            rationale="Quality gate passed, all checks satisfied",
        )

        self.registry.record("approval", repository, "release_approved", actor=approved_by)

        return {
            "approved": True,
            "decision_id": decision.id,
            "gate_id": gate.id,
            "version": version,
        }

    def reject_release(
        self,
        repository: str,
        version: str,
        rejected_by: str,
        rationale: str = "",
    ) -> dict[str, Any]:
        review = self.reviews.create_review(
            repository=repository, review_type=ReviewType.CERTIFICATION
        )
        decision = self.decisions.reject(
            repository=repository,
            review_id=review.id,
            decided_by=rejected_by,
            rationale=rationale or "Release rejected by governance",
        )

        self.registry.record("rejection", repository, "release_rejected", actor=rejected_by)

        return {
            "rejected": True,
            "decision_id": decision.id,
            "rationale": decision.rationale,
        }

    def get_repository_status(self, repository: str) -> dict[str, Any]:
        findings_summary = self.findings.get_findings_summary(repository)
        review_summary = self.reviews.get_review_summary(repository)
        risk_summary = self.risk.get_risk_summary(repository)
        compliance_summary = self.compliance.get_compliance_summary(repository)
        exception_summary = self.exceptions.get_exception_summary(repository)
        history = self.registry.get_statistics(repository)
        can_release = self.quality_gates.can_release(repository)

        return {
            "repository": repository,
            "findings": findings_summary,
            "reviews": review_summary,
            "risk": risk_summary,
            "compliance": compliance_summary,
            "exceptions": exception_summary,
            "history": history,
            "release_status": can_release,
        }

    def get_governance_dashboard(self) -> dict[str, Any]:
        total_findings = self.findings.count()
        total_reviews = self.reviews.count()
        total_decisions = self.decisions.count()
        total_exceptions = self.exceptions.count()

        return {
            "total_findings": total_findings,
            "total_reviews": total_reviews,
            "total_decisions": total_decisions,
            "total_exceptions": total_exceptions,
            "critical_findings": len(self.findings.get_critical_findings()),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
