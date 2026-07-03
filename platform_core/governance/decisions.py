"""Decision Engine - Makes governance decisions based on reviews and findings."""

from __future__ import annotations

import threading

from platform_core.governance.types import (
    Decision,
    DecisionType,
    Finding,
    FindingSeverity,
    FindingStatus,
)


class DecisionEngine:
    """Makes governance decisions based on review results and findings."""

    def __init__(self) -> None:
        self._decisions: dict[str, Decision] = {}
        self._lock = threading.RLock()

    def make_decision(
        self,
        repository: str,
        review_id: str,
        findings: list[Finding],
        decided_by: str = "governance-engine",
        auto_decide: bool = True,
    ) -> Decision:
        if auto_decide:
            decision_type = self._evaluate_findings(findings)
        else:
            decision_type = DecisionType.DEFER

        conditions: list[str] = []
        if decision_type == DecisionType.REJECT:
            critical = [f for f in findings if f.severity == FindingSeverity.CRITICAL]
            high = [f for f in findings if f.severity == FindingSeverity.HIGH]
            if critical:
                conditions.append(f"Resolve {len(critical)} critical findings")
            if high:
                conditions.append(f"Resolve {len(high)} high findings")
        elif decision_type == DecisionType.APPROVE:
            conditions.append("All findings resolved or acknowledged")

        decision = Decision(
            review_id=review_id,
            repository=repository,
            decision_type=decision_type,
            rationale=self._generate_rationale(decision_type, findings),
            decided_by=decided_by,
            conditions=conditions,
        )

        with self._lock:
            self._decisions[decision.id] = decision

        return decision

    def _evaluate_findings(self, findings: list[Finding]) -> DecisionType:
        open_findings = [f for f in findings if f.status == FindingStatus.OPEN]
        critical = [f for f in open_findings if f.severity == FindingSeverity.CRITICAL]
        high = [f for f in open_findings if f.severity == FindingSeverity.HIGH]

        if critical:
            return DecisionType.REJECT
        if high:
            return DecisionType.REJECT
        if len(open_findings) > 5:
            return DecisionType.DEFER
        return DecisionType.APPROVE

    def _generate_rationale(self, decision_type: DecisionType, findings: list[Finding]) -> str:
        open_count = len([f for f in findings if f.status == FindingStatus.OPEN])
        critical_count = len(
            [
                f
                for f in findings
                if f.severity == FindingSeverity.CRITICAL and f.status == FindingStatus.OPEN
            ]
        )
        high_count = len(
            [
                f
                for f in findings
                if f.severity == FindingSeverity.HIGH and f.status == FindingStatus.OPEN
            ]
        )

        if decision_type == DecisionType.APPROVE:
            return f"Approved: {open_count} open findings, none critical or high"
        elif decision_type == DecisionType.REJECT:
            return (
                f"Rejected: {critical_count} critical, "
                f"{high_count} high findings require resolution"
            )
        elif decision_type == DecisionType.DEFER:
            return f"Deferred: {open_count} open findings require review"
        return f"Decision: {decision_type.value}"

    def get_decision(self, decision_id: str) -> Decision | None:
        with self._lock:
            return self._decisions.get(decision_id)

    def list_decisions(
        self,
        repository: str | None = None,
        decision_type: DecisionType | None = None,
    ) -> list[Decision]:
        with self._lock:
            results = list(self._decisions.values())

        if repository is not None:
            results = [d for d in results if d.repository == repository]
        if decision_type is not None:
            results = [d for d in results if d.decision_type == decision_type]

        return results

    def get_latest_decision(self, repository: str) -> Decision | None:
        decisions = self.list_decisions(repository=repository)
        if not decisions:
            return None
        return max(decisions, key=lambda d: d.decided_at)

    def approve(
        self, repository: str, review_id: str, decided_by: str, rationale: str = ""
    ) -> Decision:
        decision = Decision(
            review_id=review_id,
            repository=repository,
            decision_type=DecisionType.APPROVE,
            rationale=rationale or "Manual approval",
            decided_by=decided_by,
        )
        with self._lock:
            self._decisions[decision.id] = decision
        return decision

    def reject(
        self, repository: str, review_id: str, decided_by: str, rationale: str = ""
    ) -> Decision:
        decision = Decision(
            review_id=review_id,
            repository=repository,
            decision_type=DecisionType.REJECT,
            rationale=rationale or "Manual rejection",
            decided_by=decided_by,
        )
        with self._lock:
            self._decisions[decision.id] = decision
        return decision

    def count(self) -> int:
        with self._lock:
            return len(self._decisions)
