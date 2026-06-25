"""Quality Gates - Enforces release gating rules."""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any

from platform_core.governance.types import (
    ComplianceStatus,
    Finding,
    FindingSeverity,
    FindingStatus,
    QualityGate,
    QualityGateResult,
)


class QualityGateEngine:
    """Enforces quality gates for package release."""

    def __init__(
        self,
        require_zero_critical: bool = True,
        require_zero_high: bool = True,
        require_security_pass: bool = True,
        require_compatibility_pass: bool = True,
        require_certification_pass: bool = True,
        require_manifest_valid: bool = True,
        require_signature_valid: bool = True,
        require_sbom_valid: bool = True,
        min_coverage: float = 0.80,
    ) -> None:
        self._require_zero_critical = require_zero_critical
        self._require_zero_high = require_zero_high
        self._require_security_pass = require_security_pass
        self._require_compatibility_pass = require_compatibility_pass
        self._require_certification_pass = require_certification_pass
        self._require_manifest_valid = require_manifest_valid
        self._require_signature_valid = require_signature_valid
        self._require_sbom_valid = require_sbom_valid
        self._min_coverage = min_coverage
        self._gates: dict[str, QualityGate] = {}
        self._lock = threading.RLock()

    def evaluate(
        self,
        repository: str,
        version: str,
        findings: list[Finding],
        coverage_percent: float = 0.0,
        security_passed: bool = True,
        compatibility_passed: bool = True,
        certification_passed: bool = True,
        manifest_valid: bool = True,
        signature_valid: bool = True,
        sbom_valid: bool = True,
    ) -> QualityGate:
        open_findings = [f for f in findings if f.status == FindingStatus.OPEN]
        critical_findings = len([f for f in open_findings if f.severity == FindingSeverity.CRITICAL])
        high_findings = len([f for f in open_findings if f.severity == FindingSeverity.HIGH])
        coverage_met = coverage_percent >= self._min_coverage

        checks = [
            {"name": "critical_findings", "passed": critical_findings == 0, "required": self._require_zero_critical},
            {"name": "high_findings", "passed": high_findings == 0, "required": self._require_zero_high},
            {"name": "coverage", "passed": coverage_met, "required": True, "value": coverage_percent, "threshold": self._min_coverage},
            {"name": "security", "passed": security_passed, "required": self._require_security_pass},
            {"name": "compatibility", "passed": compatibility_passed, "required": self._require_compatibility_pass},
            {"name": "certification", "passed": certification_passed, "required": self._require_certification_pass},
            {"name": "manifest_valid", "passed": manifest_valid, "required": self._require_manifest_valid},
            {"name": "signature_valid", "passed": signature_valid, "required": self._require_signature_valid},
            {"name": "sbom_valid", "passed": sbom_valid, "required": self._require_sbom_valid},
        ]

        required_failed = any(
            not c["passed"] for c in checks if c["required"]
        )

        has_waived = False  # Would check exception manager in production

        if required_failed:
            result = QualityGateResult.FAILED
        elif has_waived:
            result = QualityGateResult.WAIVED
        else:
            result = QualityGateResult.PASSED

        gate = QualityGate(
            repository=repository,
            version=version,
            result=result,
            checks=checks,
            critical_findings=critical_findings,
            high_findings=high_findings,
            coverage_met=coverage_met,
            security_passed=security_passed,
            compatibility_passed=compatibility_passed,
            certification_passed=certification_passed,
            manifest_valid=manifest_valid,
            signature_valid=signature_valid,
            sbom_valid=sbom_valid,
        )

        with self._lock:
            self._gates[gate.id] = gate

        return gate

    def get_gate(self, gate_id: str) -> QualityGate | None:
        with self._lock:
            return self._gates.get(gate_id)

    def list_gates(
        self,
        repository: str | None = None,
        result: QualityGateResult | None = None,
    ) -> list[QualityGate]:
        with self._lock:
            gates = list(self._gates.values())

        if repository is not None:
            gates = [g for g in gates if g.repository == repository]
        if result is not None:
            gates = [g for g in gates if g.result == result]

        return gates

    def get_latest_gate(self, repository: str) -> QualityGate | None:
        gates = self.list_gates(repository=repository)
        if not gates:
            return None
        return max(gates, key=lambda g: g.evaluated_at)

    def can_release(self, repository: str) -> dict[str, Any]:
        gate = self.get_latest_gate(repository)
        if gate is None:
            return {"can_release": False, "reason": "No quality gate evaluation found"}

        return {
            "can_release": gate.result == QualityGateResult.PASSED,
            "result": gate.result.value,
            "critical_findings": gate.critical_findings,
            "high_findings": gate.high_findings,
            "coverage_met": gate.coverage_met,
            "security_passed": gate.security_passed,
        }

    def count(self) -> int:
        with self._lock:
            return len(self._gates)
