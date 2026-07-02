"""Unit tests for Constitution Enforcer."""

from platform_core.governance.constitution import ConstitutionEnforcer


class TestConstitutionEnforcer:
    def test_init(self) -> None:
        ce = ConstitutionEnforcer()
        assert ce.count() == 0

    def test_validate_all_pass(self) -> None:
        ce = ConstitutionEnforcer()
        evidence = {
            "has_readme": True,
            "manifest_present": True,
            "manifest_valid": True,
            "api_documented": True,
            "no_shared_databases": True,
            "dependencies_declared": True,
            "version_declared": True,
            "discovery_compatible": True,
            "metadata_complete": True,
            "uses_platform_services": True,
            "service_registration": True,
            "event_driven": True,
            "event_documented": True,
            "api_versioned": True,
            "health_endpoint": True,
            "device_compatible": True,
            "ai_documented": True,
            "ai_audit_trail": True,
            "metrics_collected": True,
            "health_score_tracked": True,
            "logging_configured": True,
            "telemetry_configured": True,
            "certification_process": True,
            "quality_gates": True,
            "decision_logged": True,
            "audit_trail": True,
            "production_business_logic_in_platform_core": False,
            "repository_independence": True,
        }
        report = ce.validate("repo", evidence)
        assert report.compliant is True

    def test_validate_all_fail(self) -> None:
        ce = ConstitutionEnforcer()
        report = ce.validate("repo", {})
        assert report.compliant is False
        assert len(report.violations) > 0

    def test_validate_partial(self) -> None:
        ce = ConstitutionEnforcer()
        evidence = {"has_readme": True, "manifest_present": True}
        report = ce.validate("repo", evidence)
        assert report.articles_checked > 0
        assert report.score < 1.0

    def test_get_report(self) -> None:
        ce = ConstitutionEnforcer()
        report = ce.validate("repo")
        found = ce.get_report(report.id)
        assert found is not None

    def test_list_reports(self) -> None:
        ce = ConstitutionEnforcer()
        ce.validate("repo-a")
        ce.validate("repo-b")
        assert len(ce.list_reports()) == 2
        assert len(ce.list_reports(repository="repo-a")) == 1

    def test_get_article_status(self) -> None:
        ce = ConstitutionEnforcer()
        status = ce.get_article_status("repo", "I")
        assert status["article"] == "I"
        assert "checks" in status
