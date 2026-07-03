"""AI Governance Assistant - Reviews and suggests improvements (read-only)."""

from __future__ import annotations

import threading
from typing import Any

from platform_core.governance.types import Finding


class AIGovernanceAssistant:
    """AI-powered governance assistant for reviews and recommendations.

    The AI Assistant may:
    - Review architecture, dependencies, manifests, APIs
    - Suggest improvements
    - Estimate risks
    - Generate remediation plans

    The AI Assistant may NOT:
    - Approve releases
    - Override Governance
    - Modify repositories automatically
    - Deploy production changes
    """

    def __init__(self) -> None:
        self._reviews: dict[str, dict[str, Any]] = {}
        self._lock = threading.RLock()

    def review_architecture(self, repository: str, evidence: dict[str, Any]) -> dict[str, Any]:
        findings: list[dict[str, Any]] = []
        recommendations: list[dict[str, Any]] = []

        pattern = evidence.get("architecture_pattern", "unknown")
        if pattern == "unknown":
            findings.append(
                {
                    "severity": "medium",
                    "title": "Undetected architecture pattern",
                    "description": "Unable to determine architecture pattern",
                }
            )
            recommendations.append(
                {
                    "priority": 2,
                    "title": "Document architecture pattern",
                    "description": "Add architecture documentation to clarify the design pattern",
                }
            )

        if not evidence.get("has_documentation"):
            recommendations.append(
                {
                    "priority": 2,
                    "title": "Add architecture documentation",
                    "description": "Create architecture documentation to explain design decisions",
                }
            )

        score = 0.8 if pattern != "unknown" else 0.5
        return {
            "repository": repository,
            "review_type": "architecture",
            "score": score,
            "findings": findings,
            "recommendations": recommendations,
            "summary": f"Architecture review: {score:.0%} score",
        }

    def review_dependencies(self, repository: str, evidence: dict[str, Any]) -> dict[str, Any]:
        findings: list[dict[str, Any]] = []
        recommendations: list[dict[str, Any]] = []

        total_deps = evidence.get("total_dependencies", 0)
        outdated = evidence.get("outdated_dependencies", 0)
        vulnerable = evidence.get("vulnerable_dependencies", 0)

        if vulnerable > 0:
            findings.append(
                {
                    "severity": "critical",
                    "title": f"{vulnerable} vulnerable dependencies",
                    "description": "Vulnerable dependencies detected",
                }
            )
            recommendations.append(
                {
                    "priority": 1,
                    "title": "Update vulnerable dependencies",
                    "description": f"Update {vulnerable} vulnerable dependencies immediately",
                }
            )

        if outdated > 0:
            findings.append(
                {
                    "severity": "low",
                    "title": f"{outdated} outdated dependencies",
                    "description": "Dependencies are outdated",
                }
            )

        score = 1.0
        if vulnerable > 0:
            score -= 0.4
        if outdated > 0:
            score -= 0.1

        return {
            "repository": repository,
            "review_type": "dependencies",
            "score": round(max(score, 0.0), 2),
            "findings": findings,
            "recommendations": recommendations,
            "summary": (
                f"Dependency review: "
                f"{total_deps} total, "
                f"{vulnerable} vulnerable, "
                f"{outdated} outdated"
            ),
        }

    def review_manifest(self, repository: str, evidence: dict[str, Any]) -> dict[str, Any]:
        findings: list[dict[str, Any]] = []
        recommendations: list[dict[str, Any]] = []

        has_manifest = evidence.get("has_manifest", False)
        manifest_valid = evidence.get("manifest_valid", False)

        if not has_manifest:
            findings.append(
                {
                    "severity": "high",
                    "title": "Missing platform manifest",
                    "description": "Repository does not have a platform manifest",
                }
            )
            recommendations.append(
                {
                    "priority": 1,
                    "title": "Create platform manifest",
                    "description": "Create platform-manifest.yaml to register with the platform",
                }
            )
            score = 0.0
        elif not manifest_valid:
            findings.append(
                {
                    "severity": "medium",
                    "title": "Invalid platform manifest",
                    "description": "Platform manifest fails validation",
                }
            )
            score = 0.5
        else:
            score = 1.0

        return {
            "repository": repository,
            "review_type": "manifest",
            "score": score,
            "findings": findings,
            "recommendations": recommendations,
            "summary": f"Manifest review: {'valid' if manifest_valid else 'invalid or missing'}",
        }

    def review_api(self, repository: str, evidence: dict[str, Any]) -> dict[str, Any]:
        findings: list[dict[str, Any]] = []
        recommendations: list[dict[str, Any]] = []

        has_health = evidence.get("has_health_endpoint", False)
        has_docs = evidence.get("has_api_docs", False)
        is_versioned = evidence.get("api_versioned", False)

        if not has_health:
            findings.append(
                {
                    "severity": "medium",
                    "title": "Missing health endpoint",
                    "description": "API does not have a health check endpoint",
                }
            )
        if not has_docs:
            recommendations.append(
                {
                    "priority": 2,
                    "title": "Add API documentation",
                    "description": "Add OpenAPI/Swagger documentation",
                }
            )

        score = 0.0
        if has_health:
            score += 0.4
        if has_docs:
            score += 0.3
        if is_versioned:
            score += 0.3

        return {
            "repository": repository,
            "review_type": "api",
            "score": round(score, 2),
            "findings": findings,
            "recommendations": recommendations,
            "summary": (
                f"API review: health={has_health}, docs={has_docs}, versioned={is_versioned}"
            ),
        }

    def estimate_risk(self, repository: str, evidence: dict[str, Any]) -> dict[str, Any]:
        risk_factors: list[dict[str, Any]] = []

        if evidence.get("vulnerable_dependencies", 0) > 0:
            risk_factors.append(
                {
                    "category": "security",
                    "level": "high",
                    "reason": "Vulnerable dependencies",
                }
            )

        if not evidence.get("has_ci"):
            risk_factors.append(
                {
                    "category": "operational",
                    "level": "medium",
                    "reason": "No CI/CD pipeline",
                }
            )

        if not evidence.get("has_tests"):
            risk_factors.append(
                {"category": "quality", "level": "high", "reason": "No tests found"}
            )

        overall_risk = "low"
        if any(r["level"] == "high" for r in risk_factors):
            overall_risk = "high"
        elif any(r["level"] == "medium" for r in risk_factors):
            overall_risk = "medium"

        return {
            "repository": repository,
            "overall_risk": overall_risk,
            "risk_factors": risk_factors,
            "summary": f"Risk assessment: {overall_risk} ({len(risk_factors)} factors)",
        }

    def generate_remediation_plan(self, repository: str, findings: list[Finding]) -> dict[str, Any]:
        plan_items: list[dict[str, Any]] = []

        sorted_findings = sorted(
            findings,
            key=lambda f: {
                "critical": 0,
                "high": 1,
                "medium": 2,
                "low": 3,
                "info": 4,
            }.get(f.severity.value, 5),
        )

        for i, finding in enumerate(sorted_findings):
            plan_items.append(
                {
                    "step": i + 1,
                    "finding_id": finding.id,
                    "severity": finding.severity.value,
                    "title": finding.title,
                    "action": finding.recommendation or "Investigate and resolve",
                    "estimated_effort": "2-4 hours",
                }
            )

        return {
            "repository": repository,
            "total_items": len(plan_items),
            "plan": plan_items,
            "estimated_total_effort": f"{len(plan_items) * 3} hours",
        }

    def count(self) -> int:
        with self._lock:
            return len(self._reviews)
