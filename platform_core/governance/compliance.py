"""Compliance Engine - Validates against 9 compliance standards."""

from __future__ import annotations

import threading
from typing import Any

from platform_core.governance.types import ComplianceCheck, ComplianceReport, ComplianceStatus


class ComplianceEngine:
    """Validates repositories against compliance standards."""

    STANDARDS: dict[str, dict[str, Any]] = {
        "constitution": {
            "name": "Platform Constitution",
            "description": "Validate against the Unified Healthcare Platform Constitution",
            "checks": [
                "has_manifest",
                "manifest_valid",
                "no_shared_databases",
                "api_documented",
                "event_driven",
            ],
        },
        "manifest_spec": {
            "name": "Manifest Specification",
            "description": "Validate manifest against platform manifest spec",
            "checks": [
                "manifest_present",
                "manifest_valid_schema",
                "dependencies_declared",
                "capabilities_declared",
                "compatibility_declared",
            ],
        },
        "api_spec": {
            "name": "API Specification",
            "description": "Validate API against platform API spec",
            "checks": [
                "api_versioned",
                "api_documented",
                "health_endpoint",
                "error_handling",
                "pagination",
            ],
        },
        "package_spec": {
            "name": "Package Specification",
            "description": "Validate package against platform package spec",
            "checks": [
                "package_signed",
                "sbom_present",
                "checksum_valid",
                "dependencies_resolved",
            ],
        },
        "security_baseline": {
            "name": "Security Baseline",
            "description": "Validate security baseline requirements",
            "checks": [
                "no_hardcoded_secrets",
                "gitignore_present",
                "security_md_present",
                "dependencies_scanned",
                "auth_configured",
            ],
        },
        "coding_standards": {
            "name": "Coding Standards",
            "description": "Validate coding standards compliance",
            "checks": [
                "lint_passing",
                "type_hints",
                "docstrings",
                "naming_conventions",
            ],
        },
        "documentation_standards": {
            "name": "Documentation Standards",
            "description": "Validate documentation standards",
            "checks": [
                "readme_present",
                "readme_quality",
                "changelog_present",
                "contributing_present",
                "license_present",
            ],
        },
        "testing_standards": {
            "name": "Testing Standards",
            "description": "Validate testing standards",
            "checks": [
                "tests_present",
                "test_framework_configured",
                "test_coverage_report",
                "integration_tests",
            ],
        },
        "coverage_standards": {
            "name": "Coverage Standards",
            "description": "Validate test coverage standards",
            "checks": [
                "coverage_report_exists",
                "unit_coverage_threshold",
                "integration_coverage_threshold",
                "critical_path_coverage",
            ],
        },
    }

    def __init__(self, coverage_threshold: float = 0.80) -> None:
        self._checks: dict[str, ComplianceCheck] = {}
        self._reports: dict[str, ComplianceReport] = {}
        self._coverage_threshold = coverage_threshold
        self._lock = threading.RLock()

    def validate_standard(
        self,
        repository: str,
        standard: str,
        evidence: dict[str, Any] | None = None,
    ) -> ComplianceCheck:
        standard_def = self.STANDARDS.get(standard)
        if standard_def is None:
            return ComplianceCheck(
                repository=repository,
                standard=standard,
                status=ComplianceStatus.UNKNOWN,
            )

        evidence = evidence or {}
        checks_total = len(standard_def["checks"])
        checks_passed = 0
        details: list[dict[str, Any]] = []

        for check_name in standard_def["checks"]:
            passed = evidence.get(check_name, False)
            if passed:
                checks_passed += 1
            details.append(
                {
                    "check": check_name,
                    "passed": passed,
                }
            )

        status = ComplianceStatus.COMPLIANT
        if checks_passed == checks_total:
            status = ComplianceStatus.COMPLIANT
        elif checks_passed == 0:
            status = ComplianceStatus.NON_COMPLIANT
        else:
            status = ComplianceStatus.PARTIAL

        score = round(checks_passed / max(checks_total, 1), 3)

        check = ComplianceCheck(
            repository=repository,
            standard=standard,
            status=status,
            score=score,
            checks_passed=checks_passed,
            checks_failed=checks_total - checks_passed,
            checks_total=checks_total,
            details=details,
        )

        with self._lock:
            self._checks[check.id] = check

        return check

    def validate_all_standards(
        self, repository: str, evidence: dict[str, dict[str, Any]] | None = None
    ) -> list[ComplianceCheck]:
        evidence = evidence or {}
        checks: list[ComplianceCheck] = []
        for standard in self.STANDARDS:
            standard_evidence = evidence.get(standard, {})
            check = self.validate_standard(repository, standard, standard_evidence)
            checks.append(check)
        return checks

    def generate_report(
        self, repository: str, checks: list[ComplianceCheck] | None = None
    ) -> ComplianceReport:
        if checks is None:
            checks = self.list_checks(repository=repository)

        if not checks:
            overall_status = ComplianceStatus.UNKNOWN
            overall_score = 0.0
        else:
            total_score = sum(c.score for c in checks)
            overall_score = round(total_score / len(checks), 3)

            non_compliant = any(c.status == ComplianceStatus.NON_COMPLIANT for c in checks)
            partial = any(c.status == ComplianceStatus.PARTIAL for c in checks)

            if non_compliant:
                overall_status = ComplianceStatus.NON_COMPLIANT
            elif partial:
                overall_status = ComplianceStatus.PARTIAL
            else:
                overall_status = ComplianceStatus.COMPLIANT

        report = ComplianceReport(
            repository=repository,
            overall_status=overall_status,
            overall_score=overall_score,
            checks=checks,
            summary=f"Overall compliance: {overall_status.value} ({overall_score:.1%})",
        )

        with self._lock:
            self._reports[report.id] = report

        return report

    def get_check(self, check_id: str) -> ComplianceCheck | None:
        with self._lock:
            return self._checks.get(check_id)

    def list_checks(
        self,
        repository: str | None = None,
        standard: str | None = None,
        status: ComplianceStatus | None = None,
    ) -> list[ComplianceCheck]:
        with self._lock:
            results = list(self._checks.values())

        if repository is not None:
            results = [c for c in results if c.repository == repository]
        if standard is not None:
            results = [c for c in results if c.standard == standard]
        if status is not None:
            results = [c for c in results if c.status == status]

        return results

    def get_report(self, report_id: str) -> ComplianceReport | None:
        with self._lock:
            return self._reports.get(report_id)

    def list_reports(self, repository: str | None = None) -> list[ComplianceReport]:
        with self._lock:
            results = list(self._reports.values())
        if repository is not None:
            results = [r for r in results if r.repository == repository]
        return results

    def get_compliance_summary(self, repository: str | None = None) -> dict[str, Any]:
        checks = self.list_checks(repository=repository)
        by_standard: dict[str, str] = {}
        for c in checks:
            by_standard[c.standard] = c.status.value

        compliant_count = sum(1 for c in checks if c.status == ComplianceStatus.COMPLIANT)
        return {
            "total_checks": len(checks),
            "compliant": compliant_count,
            "non_compliant": sum(1 for c in checks if c.status == ComplianceStatus.NON_COMPLIANT),
            "partial": sum(1 for c in checks if c.status == ComplianceStatus.PARTIAL),
            "by_standard": by_standard,
        }

    def count(self) -> int:
        with self._lock:
            return len(self._checks)
