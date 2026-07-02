"""Unit tests for Compliance Engine."""

import pytest

from platform_core.governance.compliance import ComplianceEngine
from platform_core.governance.types import ComplianceStatus


class TestComplianceEngine:
    def test_init(self) -> None:
        ce = ComplianceEngine()
        assert ce.count() == 0

    def test_validate_standard_pass(self) -> None:
        ce = ComplianceEngine()
        evidence = {
            "has_manifest": True,
            "manifest_valid": True,
            "no_shared_databases": True,
            "api_documented": True,
            "event_driven": True,
        }
        check = ce.validate_standard("repo", "constitution", evidence)
        assert check.status == ComplianceStatus.COMPLIANT
        assert check.score == 1.0

    def test_validate_standard_partial(self) -> None:
        ce = ComplianceEngine()
        evidence = {
            "manifest_present": True,
            "manifest_valid_schema": True,
            "dependencies_declared": True,
            "capabilities_declared": False,
            "compatibility_declared": False,
        }
        check = ce.validate_standard("repo", "manifest_spec", evidence)
        assert check.status == ComplianceStatus.PARTIAL

    def test_validate_standard_fail(self) -> None:
        ce = ComplianceEngine()
        check = ce.validate_standard("repo", "constitution", {})
        assert check.status == ComplianceStatus.NON_COMPLIANT

    def test_validate_unknown_standard(self) -> None:
        ce = ComplianceEngine()
        check = ce.validate_standard("repo", "unknown_standard")
        assert check.status == ComplianceStatus.UNKNOWN

    def test_validate_all_standards(self) -> None:
        ce = ComplianceEngine()
        checks = ce.validate_all_standards("repo")
        assert len(checks) == len(ce.STANDARDS)

    def test_generate_report(self) -> None:
        ce = ComplianceEngine()
        checks = ce.validate_all_standards("repo")
        report = ce.generate_report("repo", checks)
        assert report.repository == "repo"
        assert report.overall_status in (
            ComplianceStatus.COMPLIANT,
            ComplianceStatus.NON_COMPLIANT,
            ComplianceStatus.PARTIAL,
        )

    def test_list_checks(self) -> None:
        ce = ComplianceEngine()
        ce.validate_standard("repo-a", "constitution", {})
        ce.validate_standard("repo-b", "constitution", {})
        assert len(ce.list_checks()) == 2
        assert len(ce.list_checks(repository="repo-a")) == 1

    def test_compliance_summary(self) -> None:
        ce = ComplianceEngine()
        ce.validate_all_standards("repo")
        summary = ce.get_compliance_summary("repo")
        assert summary["total_checks"] == len(ce.STANDARDS)
