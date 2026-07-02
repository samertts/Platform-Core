"""Unit tests for Quality Gate Engine."""

import pytest

from platform_core.governance.quality import QualityGateEngine
from platform_core.governance.types import (Finding, FindingSeverity,
                                            FindingStatus, QualityGateResult)


class TestQualityGateEngine:
    def test_init(self) -> None:
        qge = QualityGateEngine()
        assert qge.count() == 0

    def test_evaluate_pass(self) -> None:
        qge = QualityGateEngine()
        gate = qge.evaluate(
            repository="repo",
            version="1.0.0",
            findings=[],
            coverage_percent=0.90,
            security_passed=True,
        )
        assert gate.result == QualityGateResult.PASSED
        assert gate.coverage_met is True

    def test_evaluate_fail_critical(self) -> None:
        qge = QualityGateEngine()
        findings = [
            Finding(severity=FindingSeverity.CRITICAL, status=FindingStatus.OPEN),
        ]
        gate = qge.evaluate("repo", "1.0.0", findings, coverage_percent=0.90)
        assert gate.result == QualityGateResult.FAILED
        assert gate.critical_findings == 1

    def test_evaluate_fail_high(self) -> None:
        qge = QualityGateEngine()
        findings = [
            Finding(severity=FindingSeverity.HIGH, status=FindingStatus.OPEN),
        ]
        gate = qge.evaluate("repo", "1.0.0", findings, coverage_percent=0.90)
        assert gate.result == QualityGateResult.FAILED

    def test_evaluate_fail_coverage(self) -> None:
        qge = QualityGateEngine(min_coverage=0.80)
        gate = qge.evaluate("repo", "1.0.0", [], coverage_percent=0.50)
        assert gate.result == QualityGateResult.FAILED
        assert gate.coverage_met is False

    def test_evaluate_fail_security(self) -> None:
        qge = QualityGateEngine()
        gate = qge.evaluate("repo", "1.0.0", [], security_passed=False)
        assert gate.result == QualityGateResult.FAILED

    def test_evaluate_fail_manifest(self) -> None:
        qge = QualityGateEngine()
        gate = qge.evaluate("repo", "1.0.0", [], manifest_valid=False)
        assert gate.result == QualityGateResult.FAILED

    def test_get_gate(self) -> None:
        qge = QualityGateEngine()
        gate = qge.evaluate("repo", "1.0.0", [])
        found = qge.get_gate(gate.id)
        assert found is not None

    def test_list_gates(self) -> None:
        qge = QualityGateEngine()
        qge.evaluate("repo-a", "1.0.0", [])
        qge.evaluate("repo-b", "1.0.0", [])
        assert len(qge.list_gates()) == 2

    def test_can_release(self) -> None:
        qge = QualityGateEngine()
        qge.evaluate("repo", "1.0.0", [], coverage_percent=0.90, security_passed=True)
        status = qge.can_release("repo")
        assert status["can_release"] is True

    def test_cannot_release(self) -> None:
        qge = QualityGateEngine()
        status = qge.can_release("nonexistent")
        assert status["can_release"] is False
