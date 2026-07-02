"""Risk Engine - Assesses and tracks governance risks across 7 categories."""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any

from platform_core.governance.types import (Finding, FindingSeverity,
                                            RiskAssessment, RiskCategory,
                                            RiskLevel)


class RiskEngine:
    """Assesses and tracks governance risks."""

    SEVERITY_TO_RISK: dict[FindingSeverity, RiskLevel] = {
        FindingSeverity.CRITICAL: RiskLevel.CRITICAL,
        FindingSeverity.HIGH: RiskLevel.HIGH,
        FindingSeverity.MEDIUM: RiskLevel.MEDIUM,
        FindingSeverity.LOW: RiskLevel.LOW,
        FindingSeverity.INFO: RiskLevel.NEGLIGIBLE,
    }

    RISK_DESCRIPTIONS: dict[RiskCategory, dict[str, str]] = {
        RiskCategory.ARCHITECTURE: {
            "description": "Risk from architectural violations or anti-patterns",
            "impact": "Scalability, maintainability, and technical debt",
            "mitigation": "Architecture review and remediation",
        },
        RiskCategory.OPERATIONAL: {
            "description": "Risk from operational issues (monitoring, logging, health checks)",
            "impact": "System reliability and incident response",
            "mitigation": "Implement operational best practices",
        },
        RiskCategory.SECURITY: {
            "description": "Risk from security vulnerabilities or misconfigurations",
            "impact": "Data breach, unauthorized access, compliance violations",
            "mitigation": "Security audit and hardening",
        },
        RiskCategory.DEPENDENCY: {
            "description": "Risk from outdated or vulnerable dependencies",
            "impact": "Security vulnerabilities, compatibility issues",
            "mitigation": "Dependency update and audit",
        },
        RiskCategory.SCALABILITY: {
            "description": "Risk from scalability limitations",
            "impact": "Performance degradation under load",
            "mitigation": "Performance testing and optimization",
        },
        RiskCategory.HEALTHCARE_COMPLIANCE: {
            "description": "Risk from healthcare standard non-compliance",
            "impact": "Regulatory penalties, interoperability failures",
            "mitigation": "Healthcare standards audit and remediation",
        },
        RiskCategory.GOVERNMENT_READINESS: {
            "description": "Risk from government deployment readiness gaps",
            "impact": "Deployment delays, compliance failures",
            "mitigation": "Government readiness assessment",
        },
    }

    def __init__(self) -> None:
        self._assessments: dict[str, RiskAssessment] = {}
        self._lock = threading.RLock()

    def assess_risk(
        self,
        repository: str,
        category: RiskCategory,
        findings: list[Finding],
        assessed_by: str = "risk-engine",
    ) -> RiskAssessment:
        score = self._calculate_risk_score(findings)
        risk_level = self._score_to_level(score)
        info = self.RISK_DESCRIPTIONS.get(category, {})

        assessment = RiskAssessment(
            repository=repository,
            risk_category=category,
            risk_level=risk_level,
            score=score,
            description=info.get("description", ""),
            impact=info.get("impact", ""),
            likelihood=self._calculate_likelihood(findings),
            mitigation=info.get("mitigation", ""),
            assessed_by=assessed_by,
        )

        with self._lock:
            self._assessments[assessment.id] = assessment

        return assessment

    def assess_all_categories(
        self, repository: str, findings: list[Finding], assessed_by: str = "risk-engine"
    ) -> list[RiskAssessment]:
        assessments: list[RiskAssessment] = []
        for category in RiskCategory:
            relevant_findings = self._filter_findings_for_category(findings, category)
            assessment = self.assess_risk(
                repository, category, relevant_findings, assessed_by
            )
            assessments.append(assessment)
        return assessments

    def _calculate_risk_score(self, findings: list[Finding]) -> float:
        if not findings:
            return 0.0

        weights = {
            FindingSeverity.CRITICAL: 1.0,
            FindingSeverity.HIGH: 0.75,
            FindingSeverity.MEDIUM: 0.5,
            FindingSeverity.LOW: 0.25,
            FindingSeverity.INFO: 0.1,
        }

        total = sum(weights.get(f.severity, 0.1) for f in findings)
        max_possible = len(findings) * 1.0
        return round(min(total / max(max_possible, 1), 1.0), 3)

    def _score_to_level(self, score: float) -> RiskLevel:
        if score >= 0.8:
            return RiskLevel.CRITICAL
        elif score >= 0.6:
            return RiskLevel.HIGH
        elif score >= 0.4:
            return RiskLevel.MEDIUM
        elif score >= 0.2:
            return RiskLevel.LOW
        return RiskLevel.NEGLIGIBLE

    def _calculate_likelihood(self, findings: list[Finding]) -> str:
        open_count = len(findings)
        if open_count >= 5:
            return "high"
        elif open_count >= 2:
            return "medium"
        return "low"

    def _filter_findings_for_category(
        self, findings: list[Finding], category: RiskCategory
    ) -> list[Finding]:
        category_map = {
            RiskCategory.ARCHITECTURE: ["architecture", "design"],
            RiskCategory.OPERATIONAL: ["operational", "monitoring", "logging"],
            RiskCategory.SECURITY: ["security"],
            RiskCategory.DEPENDENCY: ["dependencies", "dependency"],
            RiskCategory.SCALABILITY: ["performance", "scalability"],
            RiskCategory.HEALTHCARE_COMPLIANCE: ["healthcare", "compliance"],
            RiskCategory.GOVERNMENT_READINESS: ["government", "deployment"],
        }
        keywords = category_map.get(category, [])
        return [
            f
            for f in findings
            if any(kw in f.category.lower() for kw in keywords) or not f.category
        ]

    def get_assessment(self, assessment_id: str) -> RiskAssessment | None:
        with self._lock:
            return self._assessments.get(assessment_id)

    def list_assessments(
        self,
        repository: str | None = None,
        category: RiskCategory | None = None,
        level: RiskLevel | None = None,
    ) -> list[RiskAssessment]:
        with self._lock:
            results = list(self._assessments.values())

        if repository is not None:
            results = [a for a in results if a.repository == repository]
        if category is not None:
            results = [a for a in results if a.risk_category == category]
        if level is not None:
            results = [a for a in results if a.risk_level == level]

        return results

    def get_risk_summary(self, repository: str | None = None) -> dict[str, Any]:
        assessments = self.list_assessments(repository=repository)
        by_level: dict[str, int] = {}
        by_category: dict[str, float] = {}

        for a in assessments:
            lvl = a.risk_level.value
            by_level[lvl] = by_level.get(lvl, 0) + 1
            by_category[a.risk_category.value] = a.score

        avg_score = (
            sum(a.score for a in assessments) / len(assessments) if assessments else 0.0
        )

        return {
            "total_assessments": len(assessments),
            "by_level": by_level,
            "by_category": by_category,
            "average_score": round(avg_score, 3),
            "highest_risk": max(
                (a.risk_level.value for a in assessments), default="none"
            ),
        }

    def count(self) -> int:
        with self._lock:
            return len(self._assessments)
