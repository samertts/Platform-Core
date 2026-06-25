"""Unit tests for Decision Engine."""

import pytest
from platform_core.governance.decisions import DecisionEngine
from platform_core.governance.types import DecisionType, Finding, FindingSeverity, FindingStatus


class TestDecisionEngine:
    def test_init(self) -> None:
        de = DecisionEngine()
        assert de.count() == 0

    def test_make_decision_approve(self) -> None:
        de = DecisionEngine()
        findings = [
            Finding(severity=FindingSeverity.LOW, status=FindingStatus.OPEN),
            Finding(severity=FindingSeverity.INFO, status=FindingStatus.OPEN),
        ]
        decision = de.make_decision("repo", "review-1", findings)
        assert decision.decision_type == DecisionType.APPROVE

    def test_make_decision_reject_critical(self) -> None:
        de = DecisionEngine()
        findings = [
            Finding(severity=FindingSeverity.CRITICAL, status=FindingStatus.OPEN),
        ]
        decision = de.make_decision("repo", "review-1", findings)
        assert decision.decision_type == DecisionType.REJECT

    def test_make_decision_reject_high(self) -> None:
        de = DecisionEngine()
        findings = [
            Finding(severity=FindingSeverity.HIGH, status=FindingStatus.OPEN),
        ]
        decision = de.make_decision("repo", "review-1", findings)
        assert decision.decision_type == DecisionType.REJECT

    def test_make_decision_defer(self) -> None:
        de = DecisionEngine()
        findings = [
            Finding(severity=FindingSeverity.MEDIUM, status=FindingStatus.OPEN) for _ in range(6)
        ]
        decision = de.make_decision("repo", "review-1", findings)
        assert decision.decision_type == DecisionType.DEFER

    def test_manual_decision(self) -> None:
        de = DecisionEngine()
        decision = de.make_decision("repo", "review-1", [], auto_decide=False)
        assert decision.decision_type == DecisionType.DEFER

    def test_approve(self) -> None:
        de = DecisionEngine()
        decision = de.approve("repo", "review-1", "alice", "Looks good")
        assert decision.decision_type == DecisionType.APPROVE
        assert decision.decided_by == "alice"

    def test_reject(self) -> None:
        de = DecisionEngine()
        decision = de.reject("repo", "review-1", "bob", "Needs work")
        assert decision.decision_type == DecisionType.REJECT

    def test_list_decisions(self) -> None:
        de = DecisionEngine()
        de.approve("repo-a", "r1", "alice")
        de.reject("repo-b", "r2", "bob")
        assert len(de.list_decisions()) == 2
        assert len(de.list_decisions(repository="repo-a")) == 1

    def test_get_latest_decision(self) -> None:
        de = DecisionEngine()
        de.approve("repo", "r1", "alice")
        latest = de.get_latest_decision("repo")
        assert latest is not None

    def test_get_latest_decision_none(self) -> None:
        de = DecisionEngine()
        assert de.get_latest_decision("nonexistent") is None
