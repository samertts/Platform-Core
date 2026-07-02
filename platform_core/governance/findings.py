"""Finding Manager - Finding lifecycle management."""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from typing import Any

from platform_core.governance.types import Finding, FindingSeverity, FindingStatus


class FindingManager:
    """Manages the lifecycle of governance findings."""

    def __init__(self) -> None:
        self._findings: dict[str, Finding] = {}
        self._lock = threading.RLock()

    def create_finding(
        self,
        repository: str,
        severity: FindingSeverity,
        category: str,
        title: str,
        description: str,
        root_cause: str = "",
        evidence: str = "",
        recommendation: str = "",
        owner: str = "",
        priority: int = 0,
        review_id: str = "",
    ) -> Finding:
        finding = Finding(
            review_id=review_id,
            repository=repository,
            severity=severity,
            status=FindingStatus.OPEN,
            category=category,
            title=title,
            description=description,
            root_cause=root_cause,
            evidence=evidence,
            recommendation=recommendation,
            owner=owner,
            priority=priority,
        )
        with self._lock:
            self._findings[finding.id] = finding
        return finding

    def get_finding(self, finding_id: str) -> Finding | None:
        with self._lock:
            return self._findings.get(finding_id)

    def update_status(self, finding_id: str, status: FindingStatus) -> Finding | None:
        with self._lock:
            finding = self._findings.get(finding_id)
            if finding is None:
                return None
            finding.status = status
            finding.updated_at = datetime.now(UTC)
            if status == FindingStatus.RESOLVED:
                finding.resolved_at = datetime.now(UTC)
            return finding

    def update_finding(self, finding_id: str, **kwargs: Any) -> Finding | None:
        with self._lock:
            finding = self._findings.get(finding_id)
            if finding is None:
                return None
            for key, value in kwargs.items():
                if hasattr(finding, key):
                    setattr(finding, key, value)
            finding.updated_at = datetime.now(UTC)
            return finding

    def delete_finding(self, finding_id: str) -> bool:
        with self._lock:
            if finding_id in self._findings:
                del self._findings[finding_id]
                return True
            return False

    def list_findings(
        self,
        repository: str | None = None,
        severity: FindingSeverity | None = None,
        status: FindingStatus | None = None,
        category: str | None = None,
    ) -> list[Finding]:
        with self._lock:
            results = list(self._findings.values())

        if repository is not None:
            results = [f for f in results if f.repository == repository]
        if severity is not None:
            results = [f for f in results if f.severity == severity]
        if status is not None:
            results = [f for f in results if f.status == status]
        if category is not None:
            results = [f for f in results if f.category == category]

        return results

    def get_findings_summary(self, repository: str | None = None) -> dict[str, Any]:
        findings = self.list_findings(repository=repository)
        by_severity: dict[str, int] = {}
        by_status: dict[str, int] = {}
        by_category: dict[str, int] = {}

        for f in findings:
            sev = f.severity.value
            by_severity[sev] = by_severity.get(sev, 0) + 1
            stat = f.status.value
            by_status[stat] = by_status.get(stat, 0) + 1
            cat = f.category or "uncategorized"
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total": len(findings),
            "by_severity": by_severity,
            "by_status": by_status,
            "by_category": by_category,
            "critical_count": by_severity.get("critical", 0),
            "high_count": by_severity.get("high", 0),
            "open_count": by_status.get("open", 0),
        }

    def get_critical_findings(self, repository: str | None = None) -> list[Finding]:
        return self.list_findings(
            repository=repository,
            severity=FindingSeverity.CRITICAL,
            status=FindingStatus.OPEN,
        )

    def has_blocking_findings(self, repository: str) -> bool:
        critical = self.list_findings(
            repository=repository,
            severity=FindingSeverity.CRITICAL,
            status=FindingStatus.OPEN,
        )
        high = self.list_findings(
            repository=repository,
            severity=FindingSeverity.HIGH,
            status=FindingStatus.OPEN,
        )
        return len(critical) > 0 or len(high) > 0

    def count(self) -> int:
        with self._lock:
            return len(self._findings)

    def clear(self) -> None:
        with self._lock:
            self._findings.clear()
