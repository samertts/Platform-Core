"""Unit tests for Recommendation Engine."""

import pytest
from platform_core.governance.recommendations import RecommendationEngine
from platform_core.governance.types import Finding, FindingSeverity


class TestRecommendationEngine:
    def test_init(self) -> None:
        re = RecommendationEngine()
        assert re.count() == 0

    def test_generate_recommendations(self) -> None:
        re = RecommendationEngine()
        findings = [
            Finding(severity=FindingSeverity.CRITICAL, title="Critical issue", category="security"),
            Finding(severity=FindingSeverity.HIGH, title="High issue", category="testing"),
            Finding(severity=FindingSeverity.LOW, title="Low issue", category="documentation"),
        ]
        recs = re.generate_recommendations(findings, "repo")
        assert len(recs) == 3
        assert recs[0].priority == 1  # Critical first
        assert recs[2].priority == 4  # Low last

    def test_prioritize(self) -> None:
        re = RecommendationEngine()
        recs = [
            re.generate_recommendations([Finding(severity=FindingSeverity.LOW, title="l")], "r")[0],
            re.generate_recommendations([Finding(severity=FindingSeverity.CRITICAL, title="c")], "r")[0],
        ]
        prioritized = re.prioritize(recs)
        assert prioritized[0].priority == 1

    def test_group_by_category(self) -> None:
        re = RecommendationEngine()
        findings = [
            Finding(severity=FindingSeverity.HIGH, title="t", category="security"),
            Finding(severity=FindingSeverity.MEDIUM, title="t", category="testing"),
            Finding(severity=FindingSeverity.LOW, title="t", category="security"),
        ]
        recs = re.generate_recommendations(findings, "repo")
        groups = re.group_by_category(recs)
        assert "security" in groups
        assert "testing" in groups

    def test_estimate_total_effort(self) -> None:
        re = RecommendationEngine()
        findings = [
            Finding(severity=FindingSeverity.HIGH, title="t", category="security"),
            Finding(severity=FindingSeverity.MEDIUM, title="t", category="testing"),
        ]
        recs = re.generate_recommendations(findings, "repo")
        effort = re.estimate_total_effort(recs)
        assert "total_hours" in effort
        assert effort["total_hours"] > 0

    def test_empty_findings(self) -> None:
        re = RecommendationEngine()
        recs = re.generate_recommendations([], "repo")
        assert len(recs) == 0
