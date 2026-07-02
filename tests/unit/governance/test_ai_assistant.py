"""Unit tests for AI Governance Assistant."""

import pytest

from platform_core.governance.ai_assistant import AIGovernanceAssistant
from platform_core.governance.types import Finding, FindingSeverity


class TestAIGovernanceAssistant:
    def test_init(self) -> None:
        ai = AIGovernanceAssistant()
        assert ai is not None

    def test_review_architecture(self) -> None:
        ai = AIGovernanceAssistant()
        result = ai.review_architecture(
            "repo", {"architecture_pattern": "microservices"}
        )
        assert result["score"] > 0
        assert result["review_type"] == "architecture"

    def test_review_architecture_unknown(self) -> None:
        ai = AIGovernanceAssistant()
        result = ai.review_architecture("repo", {})
        assert result["score"] == 0.5

    def test_review_dependencies(self) -> None:
        ai = AIGovernanceAssistant()
        result = ai.review_dependencies(
            "repo", {"total_dependencies": 10, "vulnerable_dependencies": 2}
        )
        assert result["review_type"] == "dependencies"
        assert len(result["findings"]) > 0

    def test_review_manifest_present(self) -> None:
        ai = AIGovernanceAssistant()
        result = ai.review_manifest(
            "repo", {"has_manifest": True, "manifest_valid": True}
        )
        assert result["score"] == 1.0

    def test_review_manifest_missing(self) -> None:
        ai = AIGovernanceAssistant()
        result = ai.review_manifest("repo", {"has_manifest": False})
        assert result["score"] == 0.0
        assert len(result["findings"]) > 0

    def test_review_api(self) -> None:
        ai = AIGovernanceAssistant()
        result = ai.review_api(
            "repo",
            {
                "has_health_endpoint": True,
                "has_api_docs": True,
                "api_versioned": True,
            },
        )
        assert result["score"] == 1.0

    def test_estimate_risk(self) -> None:
        ai = AIGovernanceAssistant()
        result = ai.estimate_risk(
            "repo", {"vulnerable_dependencies": 1, "has_ci": False}
        )
        assert result["overall_risk"] in ("high", "medium", "low")

    def test_generate_remediation_plan(self) -> None:
        ai = AIGovernanceAssistant()
        findings = [
            Finding(
                severity=FindingSeverity.CRITICAL,
                title="Critical",
                recommendation="Fix now",
            ),
            Finding(
                severity=FindingSeverity.LOW, title="Low", recommendation="Fix later"
            ),
        ]
        plan = ai.generate_remediation_plan("repo", findings)
        assert plan["total_items"] == 2
        assert plan["plan"][0]["severity"] == "critical"
