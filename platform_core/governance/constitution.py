"""Constitution Enforcement.Auto-validates against the Unified Healthcare Platform Constitution."""

from __future__ import annotations

import threading
from typing import Any

from platform_core.governance.types import (
    ConstitutionReport,
    Finding,
    FindingSeverity,
    FindingStatus,
    Recommendation,
)


class ConstitutionEnforcer:
    """Auto-validates repositories against the Platform Constitution."""

    ARTICLES: dict[str, dict[str, Any]] = {
        "I": {
            "title": "Platform Principles",
            "checks": ["has_readme", "manifest_present", "api_documented"],
        },
        "II": {
            "title": "Repository Governance",
            "checks": ["manifest_valid", "dependencies_declared", "version_declared"],
        },
        "III": {
            "title": "Platform Knowledge",
            "checks": ["discovery_compatible", "metadata_complete"],
        },
        "IV": {
            "title": "Manifest Standard",
            "checks": ["manifest_present", "manifest_valid_schema"],
        },
        "V": {
            "title": "Shared Platform Services",
            "checks": ["uses_platform_services", "service_registration"],
        },
        "VI": {
            "title": "Event Governance",
            "checks": ["event_driven", "event_documented"],
        },
        "VII": {
            "title": "API Governance",
            "checks": ["api_versioned", "api_documented", "health_endpoint"],
        },
        "VIII": {
            "title": "Device Platform",
            "checks": ["device_compatible"],
        },
        "IX": {
            "title": "AI Governance",
            "checks": ["ai_documented", "ai_audit_trail"],
        },
        "X": {
            "title": "Self Evolution",
            "checks": ["metrics_collected", "health_score_tracked"],
        },
        "XI": {
            "title": "Operational Intelligence",
            "checks": ["logging_configured", "telemetry_configured"],
        },
        "XII": {
            "title": "Certification",
            "checks": ["certification_process", "quality_gates"],
        },
        "XV": {
            "title": "Platform Memory",
            "checks": ["decision_logged", "audit_trail"],
        },
        "XVII": {
            "title": "Prohibitions",
            "checks": [
                "no_shared_databases",
                "no_production_business_logic_in_platform_core",
                "repository_independence",
            ],
        },
    }

    PROHIBITED_PATTERNS = [
        {
            "pattern": "shared_database",
            "severity": FindingSeverity.CRITICAL,
            "message": "Shared database detected (Prohibition XVII)",
        },
        {
            "pattern": "production_business_logic",
            "severity": FindingSeverity.HIGH,
            "message": "Production business logic in platform core (Prohibition XVII)",
        },
    ]

    def __init__(self) -> None:
        self._reports: dict[str, ConstitutionReport] = {}
        self._lock = threading.RLock()

    def validate(
        self,
        repository: str,
        evidence: dict[str, Any] | None = None,
    ) -> ConstitutionReport:
        evidence = evidence or {}
        violations: list[Finding] = []
        recommendations: list[Recommendation] = []
        articles_checked = 0
        articles_passed = 0

        for article_id, article in self.ARTICLES.items():
            articles_checked += 1
            article_passed = True

            for check in article["checks"]:
                passed = evidence.get(check, False)
                if not passed:
                    article_passed = False
                    finding = Finding(
                        repository=repository,
                        severity=FindingSeverity.MEDIUM,
                        status=FindingStatus.OPEN,
                        category="constitution",
                        title=f"Constitution Article {article_id}: {article['title']}",
                        description=f"Check '{check}' failed for Article {article_id}",
                        root_cause=f"Repository does not satisfy Constitution Article {article_id}",
                        recommendation=f"Implement {check} to comply with Article {article_id}",
                    )
                    violations.append(finding)
                    recommendations.append(
                        Recommendation(
                            finding_id=finding.id,
                            repository=repository,
                            category="constitution",
                            priority=3,
                            title=f"Comply with Article {article_id}: {article['title']}",
                            description=f"Implement {check}",
                            estimated_effort="2-4 hours",
                        )
                    )

            if article_passed:
                articles_passed += 1

        score = round(articles_passed / max(articles_checked, 1), 3)
        compliant = score >= 0.8

        report = ConstitutionReport(
            repository=repository,
            compliant=compliant,
            score=score,
            articles_checked=articles_checked,
            articles_passed=articles_passed,
            violations=violations,
            recommendations=recommendations,
            summary=(
                "Constitution compliance: "
                f"{articles_passed}/{articles_checked} "
                f"articles passed ({score:.1%})"
            ),
        )

        with self._lock:
            self._reports[report.id] = report

        return report

    def get_report(self, report_id: str) -> ConstitutionReport | None:
        with self._lock:
            return self._reports.get(report_id)

    def list_reports(self, repository: str | None = None) -> list[ConstitutionReport]:
        with self._lock:
            results = list(self._reports.values())
        if repository is not None:
            results = [r for r in results if r.repository == repository]
        return results

    def get_article_status(self, repository: str, article_id: str) -> dict[str, Any]:
        article = self.ARTICLES.get(article_id)
        if article is None:
            return {"error": f"Article {article_id} not found"}
        return {
            "article": article_id,
            "title": article["title"],
            "checks": article["checks"],
        }

    def count(self) -> int:
        with self._lock:
            return len(self._reports)
