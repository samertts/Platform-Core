"""Governance Registry - Maintains audit history of all governance actions."""

from __future__ import annotations

import threading
from datetime import datetime
from typing import Any

from platform_core.governance.types import GovernanceRecord


class GovernanceRegistry:
    """Maintains a complete audit history of all governance actions."""

    def __init__(self) -> None:
        self._records: dict[str, GovernanceRecord] = {}
        self._lock = threading.RLock()

    def record(
        self,
        record_type: str,
        repository: str,
        action: str,
        actor: str = "system",
        details: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> GovernanceRecord:
        rec = GovernanceRecord(
            record_type=record_type,
            repository=repository,
            action=action,
            actor=actor,
            details=details or {},
            metadata=metadata or {},
        )
        with self._lock:
            self._records[rec.id] = rec
        return rec

    def get_record(self, record_id: str) -> GovernanceRecord | None:
        with self._lock:
            return self._records.get(record_id)

    def list_records(
        self,
        repository: str | None = None,
        record_type: str | None = None,
        actor: str | None = None,
        since: datetime | None = None,
    ) -> list[GovernanceRecord]:
        with self._lock:
            results = list(self._records.values())

        if repository is not None:
            results = [r for r in results if r.repository == repository]
        if record_type is not None:
            results = [r for r in results if r.record_type == record_type]
        if actor is not None:
            results = [r for r in results if r.actor == actor]
        if since is not None:
            results = [r for r in results if r.timestamp >= since]

        return results

    def get_repository_history(self, repository: str) -> list[GovernanceRecord]:
        records = self.list_records(repository=repository)
        return sorted(records, key=lambda r: r.timestamp)

    def get_actor_history(self, actor: str) -> list[GovernanceRecord]:
        records = self.list_records(actor=actor)
        return sorted(records, key=lambda r: r.timestamp)

    def get_statistics(self, repository: str | None = None) -> dict[str, Any]:
        records = self.list_records(repository=repository)
        by_type: dict[str, int] = {}
        by_actor: dict[str, int] = {}
        for r in records:
            by_type[r.record_type] = by_type.get(r.record_type, 0) + 1
            by_actor[r.actor] = by_actor.get(r.actor, 0) + 1

        return {
            "total_records": len(records),
            "by_type": by_type,
            "by_actor": by_actor,
        }

    def count(self) -> int:
        with self._lock:
            return len(self._records)

    def clear(self) -> None:
        with self._lock:
            self._records.clear()
