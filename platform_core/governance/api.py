"""Governance REST API - Exposes governance operations via HTTP endpoints."""

from __future__ import annotations

from typing import Any

from platform_core.governance.engine import GovernanceEngine
from platform_core.governance.types import (
    DecisionType,
    ExceptionType,
    FindingSeverity,
    FindingStatus,
    QualityGateResult,
    ReviewType,
)


class GovernanceAPI:
    """REST API layer for governance operations."""

    def __init__(self, engine: GovernanceEngine | None = None) -> None:
        self._engine = engine or GovernanceEngine()

    @property
    def engine(self) -> GovernanceEngine:
        return self._engine

    def review_repository(
        self, repository: str, evidence: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return self._engine.run_full_review(repository, evidence)

    def approve_release(
        self,
        repository: str,
        version: str,
        approved_by: str,
        evidence: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._engine.approve_release(repository, version, approved_by, evidence)

    def reject_release(
        self,
        repository: str,
        version: str,
        rejected_by: str,
        rationale: str = "",
    ) -> dict[str, Any]:
        return self._engine.reject_release(repository, version, rejected_by, rationale)

    def get_repository_status(self, repository: str) -> dict[str, Any]:
        return self._engine.get_repository_status(repository)

    def get_dashboard(self) -> dict[str, Any]:
        return self._engine.get_governance_dashboard()

    def get_findings(
        self,
        repository: str | None = None,
        severity: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        sev = FindingSeverity(severity) if severity else None
        stat = FindingStatus(status) if status else None
        findings = self._engine.findings.list_findings(
            repository=repository, severity=sev, status=stat
        )
        return [
            {
                "id": f.id,
                "repository": f.repository,
                "severity": f.severity.value,
                "status": f.status.value,
                "category": f.category,
                "title": f.title,
                "description": f.description,
                "root_cause": f.root_cause,
                "recommendation": f.recommendation,
            }
            for f in findings
        ]

    def create_finding(
        self,
        repository: str,
        severity: str,
        category: str,
        title: str,
        description: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        finding = self._engine.findings.create_finding(
            repository=repository,
            severity=FindingSeverity(severity),
            category=category,
            title=title,
            description=description,
            **kwargs,
        )
        return {"id": finding.id, "severity": finding.severity.value, "status": finding.status.value}

    def get_compliance(self, repository: str) -> dict[str, Any]:
        checks = self._engine.compliance.validate_all_standards(repository)
        report = self._engine.compliance.generate_report(repository, checks)
        return {
            "repository": repository,
            "status": report.overall_status.value,
            "score": report.overall_score,
            "checks": len(report.checks),
        }

    def get_risk_assessment(self, repository: str) -> dict[str, Any]:
        return self._engine.risk.get_risk_summary(repository)

    def get_quality_gate(
        self,
        repository: str,
        version: str,
        evidence: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        evidence = evidence or {}
        findings = self._engine.findings.list_findings(repository=repository)
        gate = self._engine.quality_gates.evaluate(
            repository=repository,
            version=version,
            findings=findings,
            coverage_percent=evidence.get("coverage_percent", 0.0),
            security_passed=evidence.get("security_passed", True),
            manifest_valid=evidence.get("manifest_valid", True),
            signature_valid=evidence.get("signature_valid", True),
            sbom_valid=evidence.get("sbom_valid", True),
        )
        return {
            "id": gate.id,
            "result": gate.result.value,
            "critical_findings": gate.critical_findings,
            "high_findings": gate.high_findings,
            "coverage_met": gate.coverage_met,
            "checks": gate.checks,
        }

    def get_constitution_report(
        self, repository: str, evidence: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        report = self._engine.constitution.validate(repository, evidence)
        return {
            "repository": repository,
            "compliant": report.compliant,
            "score": report.score,
            "articles_checked": report.articles_checked,
            "articles_passed": report.articles_passed,
            "violations": len(report.violations),
        }

    def get_ai_review(
        self, repository: str, evidence: dict[str, Any]
    ) -> dict[str, Any]:
        arch_review = self._engine.ai_assistant.review_architecture(repository, evidence)
        dep_review = self._engine.ai_assistant.review_dependencies(repository, evidence)
        manifest_review = self._engine.ai_assistant.review_manifest(repository, evidence)
        api_review = self._engine.ai_assistant.review_api(repository, evidence)
        risk = self._engine.ai_assistant.estimate_risk(repository, evidence)

        return {
            "repository": repository,
            "architecture": arch_review,
            "dependencies": dep_review,
            "manifest": manifest_review,
            "api": api_review,
            "risk": risk,
        }

    def get_recommendations(self, repository: str) -> list[dict[str, Any]]:
        findings = self._engine.findings.list_findings(repository=repository)
        recs = self._engine.recommendations.generate_recommendations(findings, repository)
        return [
            {
                "id": r.id,
                "category": r.category,
                "priority": r.priority,
                "title": r.title,
                "description": r.description,
                "estimated_effort": r.estimated_effort,
            }
            for r in recs
        ]
