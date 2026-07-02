"""Unit tests for Governance API."""

import pytest

from platform_core.governance.api import GovernanceAPI


class TestGovernanceAPI:
    def test_init(self) -> None:
        api = GovernanceAPI()
        assert api is not None

    def test_review_repository(self) -> None:
        api = GovernanceAPI()
        result = api.review_repository("repo")
        assert "constitution" in result

    def test_approve_release(self) -> None:
        api = GovernanceAPI()
        result = api.approve_release(
            "repo",
            "1.0.0",
            "alice",
            evidence={
                "coverage_percent": 0.90,
                "security_passed": True,
                "manifest_valid": True,
            },
        )
        assert result["approved"] is True

    def test_reject_release(self) -> None:
        api = GovernanceAPI()
        result = api.reject_release("repo", "1.0.0", "bob", "Reason")
        assert result["rejected"] is True

    def test_get_repository_status(self) -> None:
        api = GovernanceAPI()
        status = api.get_repository_status("repo")
        assert "findings" in status

    def test_get_dashboard(self) -> None:
        api = GovernanceAPI()
        dashboard = api.get_dashboard()
        assert "total_findings" in dashboard

    def test_get_findings(self) -> None:
        api = GovernanceAPI()
        findings = api.get_findings()
        assert isinstance(findings, list)

    def test_create_finding(self) -> None:
        api = GovernanceAPI()
        result = api.create_finding(
            "repo",
            "high",
            "security",
            "Test finding",
            "Description",
        )
        assert "id" in result
        assert result["severity"] == "high"

    def test_get_compliance(self) -> None:
        api = GovernanceAPI()
        result = api.get_compliance("repo")
        assert "status" in result

    def test_get_risk_assessment(self) -> None:
        api = GovernanceAPI()
        result = api.get_risk_assessment("repo")
        assert "total_assessments" in result

    def test_get_quality_gate(self) -> None:
        api = GovernanceAPI()
        result = api.get_quality_gate("repo", "1.0.0")
        assert "result" in result

    def test_get_constitution_report(self) -> None:
        api = GovernanceAPI()
        result = api.get_constitution_report("repo")
        assert "compliant" in result

    def test_get_ai_review(self) -> None:
        api = GovernanceAPI()
        result = api.get_ai_review("repo", {"has_manifest": True})
        assert "architecture" in result
        assert "dependencies" in result

    def test_get_recommendations(self) -> None:
        api = GovernanceAPI()
        recs = api.get_recommendations("repo")
        assert isinstance(recs, list)
