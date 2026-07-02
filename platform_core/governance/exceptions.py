"""Exception Manager - Manages governance exceptions, waivers, and overrides."""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from typing import Any

from platform_core.governance.types import Exception, ExceptionType, Waiver


class ExceptionManager:
    """Manages governance exceptions and waivers."""

    def __init__(self) -> None:
        self._exceptions: dict[str, Exception] = {}
        self._waivers: dict[str, Waiver] = {}
        self._lock = threading.RLock()

    def create_exception(
        self,
        repository: str,
        exception_type: ExceptionType,
        reason: str,
        approved_by: str,
        finding_ids: list[str] | None = None,
        conditions: list[str] | None = None,
        expires_at: datetime | None = None,
    ) -> Exception:
        exc = Exception(
            repository=repository,
            exception_type=exception_type,
            reason=reason,
            approved_by=approved_by,
            finding_ids=finding_ids or [],
            conditions=conditions or [],
            expires_at=expires_at,
        )
        with self._lock:
            self._exceptions[exc.id] = exc
        return exc

    def get_exception(self, exception_id: str) -> Exception | None:
        with self._lock:
            return self._exceptions.get(exception_id)

    def revoke_exception(self, exception_id: str) -> bool:
        with self._lock:
            exc = self._exceptions.get(exception_id)
            if exc is None:
                return False
            exc.active = False
            return True

    def list_exceptions(
        self,
        repository: str | None = None,
        exception_type: ExceptionType | None = None,
        active_only: bool = True,
    ) -> list[Exception]:
        with self._lock:
            results = list(self._exceptions.values())

        if active_only:
            results = [e for e in results if e.active]
        if repository is not None:
            results = [e for e in results if e.repository == repository]
        if exception_type is not None:
            results = [e for e in results if e.exception_type == exception_type]

        return results

    def has_active_exception(
        self, repository: str, exception_type: ExceptionType | None = None
    ) -> bool:
        exceptions = self.list_exceptions(
            repository=repository,
            exception_type=exception_type,
            active_only=True,
        )
        now = datetime.now(UTC)
        for exc in exceptions:
            if exc.expires_at is None or exc.expires_at > now:
                return True
        return False

    def create_waiver(
        self,
        finding_id: str,
        repository: str,
        reason: str,
        waived_by: str,
        conditions: list[str] | None = None,
        expires_at: datetime | None = None,
    ) -> Waiver:
        waiver = Waiver(
            finding_id=finding_id,
            repository=repository,
            reason=reason,
            waived_by=waived_by,
            conditions=conditions or [],
            expires_at=expires_at,
        )
        with self._lock:
            self._waivers[waiver.id] = waiver
        return waiver

    def get_waiver(self, waiver_id: str) -> Waiver | None:
        with self._lock:
            return self._waivers.get(waiver_id)

    def revoke_waiver(self, waiver_id: str) -> bool:
        with self._lock:
            waiver = self._waivers.get(waiver_id)
            if waiver is None:
                return False
            waiver.active = False
            return True

    def list_waivers(
        self,
        repository: str | None = None,
        finding_id: str | None = None,
        active_only: bool = True,
    ) -> list[Waiver]:
        with self._lock:
            results = list(self._waivers.values())

        if active_only:
            results = [w for w in results if w.active]
        if repository is not None:
            results = [w for w in results if w.repository == repository]
        if finding_id is not None:
            results = [w for w in results if w.finding_id == finding_id]

        return results

    def is_finding_waived(self, finding_id: str) -> bool:
        waivers = self.list_waivers(finding_id=finding_id, active_only=True)
        now = datetime.now(UTC)
        for waiver in waivers:
            if waiver.expires_at is None or waiver.expires_at > now:
                return True
        return False

    def get_exception_summary(self, repository: str | None = None) -> dict[str, Any]:
        exceptions = self.list_exceptions(repository=repository, active_only=False)
        active = [e for e in exceptions if e.active]
        by_type: dict[str, int] = {}
        for e in active:
            t = e.exception_type.value
            by_type[t] = by_type.get(t, 0) + 1
        return {
            "total": len(exceptions),
            "active": len(active),
            "by_type": by_type,
        }

    def count(self) -> int:
        with self._lock:
            return len(self._exceptions) + len(self._waivers)
