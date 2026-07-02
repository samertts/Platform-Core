"""Unit tests for Governance Engine."""

from platform_core.governance.engine import GovernanceEngine


class TestGovernanceEngine:
    def test_init(self) -> None:
        ge = GovernanceEngine()
        assert ge is not None

    def test_run_full_review(self) -> None:
        ge = GovernanceEngine()
        results = ge.run_full_review("repo")
        assert "constitution" in results
        assert "compliance" in results
        assert "quality_gate" in results

    def test_approve_release(self) -> None:
        ge = GovernanceEngine()
        result = ge.approve_release(
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
        ge = GovernanceEngine()
        result = ge.reject_release("repo", "1.0.0", "bob", "Needs work")
        assert result["rejected"] is True

    def test_get_repository_status(self) -> None:
        ge = GovernanceEngine()
        status = ge.get_repository_status("repo")
        assert "findings" in status
        assert "reviews" in status
        assert "compliance" in status

    def test_get_governance_dashboard(self) -> None:
        ge = GovernanceEngine()
        dashboard = ge.get_governance_dashboard()
        assert "total_findings" in dashboard
        assert "total_reviews" in dashboard
