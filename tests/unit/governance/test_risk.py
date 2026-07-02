"""Unit tests for Risk Engine."""

import pytest

from platform_core.governance.risk import RiskEngine
from platform_core.governance.types import (Finding, FindingSeverity,
                                            RiskCategory, RiskLevel)


class TestRiskEngine:
    def test_init(self) -> None:
        re = RiskEngine()
        assert re.count() == 0

    def test_assess_risk(self) -> None:
        re = RiskEngine()
        findings = [
            Finding(severity=FindingSeverity.CRITICAL, category="security"),
            Finding(severity=FindingSeverity.HIGH, category="security"),
        ]
        assessment = re.assess_risk("repo", RiskCategory.SECURITY, findings)
        assert assessment.risk_category == RiskCategory.SECURITY
        assert assessment.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH)

    def test_assess_risk_no_findings(self) -> None:
        re = RiskEngine()
        assessment = re.assess_risk("repo", RiskCategory.ARCHITECTURE, [])
        assert assessment.risk_level == RiskLevel.NEGLIGIBLE
        assert assessment.score == 0.0

    def test_assess_all_categories(self) -> None:
        re = RiskEngine()
        assessments = re.assess_all_categories("repo", [])
        assert len(assessments) == len(RiskCategory)

    def test_get_assessment(self) -> None:
        re = RiskEngine()
        a = re.assess_risk("repo", RiskCategory.SECURITY, [])
        found = re.get_assessment(a.id)
        assert found is not None

    def test_list_assessments(self) -> None:
        re = RiskEngine()
        re.assess_risk("repo-a", RiskCategory.SECURITY, [])
        re.assess_risk("repo-b", RiskCategory.ARCHITECTURE, [])
        assert len(re.list_assessments()) == 2
        assert len(re.list_assessments(repository="repo-a")) == 1

    def test_risk_summary(self) -> None:
        re = RiskEngine()
        re.assess_risk(
            "repo",
            RiskCategory.SECURITY,
            [
                Finding(severity=FindingSeverity.HIGH, category="security"),
            ],
        )
        summary = re.get_risk_summary("repo")
        assert summary["total_assessments"] == 1
