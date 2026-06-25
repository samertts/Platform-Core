"""Unit tests for Exception Manager."""

import pytest
from platform_core.governance.exceptions import ExceptionManager
from platform_core.governance.types import ExceptionType


class TestExceptionManager:
    def test_init(self) -> None:
        em = ExceptionManager()
        assert em.count() == 0

    def test_create_exception(self) -> None:
        em = ExceptionManager()
        exc = em.create_exception(
            repository="repo", exception_type=ExceptionType.SECURITY,
            reason="Legacy code", approved_by="alice",
        )
        assert exc.repository == "repo"
        assert exc.active is True

    def test_get_exception(self) -> None:
        em = ExceptionManager()
        exc = em.create_exception("repo", ExceptionType.COMPLIANCE, "reason", "alice")
        found = em.get_exception(exc.id)
        assert found is not None

    def test_revoke_exception(self) -> None:
        em = ExceptionManager()
        exc = em.create_exception("repo", ExceptionType.SECURITY, "r", "a")
        assert em.revoke_exception(exc.id) is True
        assert em.get_exception(exc.id).active is False

    def test_list_exceptions(self) -> None:
        em = ExceptionManager()
        em.create_exception("repo-a", ExceptionType.SECURITY, "r", "a")
        em.create_exception("repo-b", ExceptionType.COMPLIANCE, "r", "a")
        assert len(em.list_exceptions()) == 2
        assert len(em.list_exceptions(repository="repo-a")) == 1

    def test_has_active_exception(self) -> None:
        em = ExceptionManager()
        em.create_exception("repo", ExceptionType.SECURITY, "r", "a")
        assert em.has_active_exception("repo") is True

    def test_no_active_exception(self) -> None:
        em = ExceptionManager()
        assert em.has_active_exception("nonexistent") is False

    def test_create_waiver(self) -> None:
        em = ExceptionManager()
        waiver = em.create_waiver(
            finding_id="f1", repository="repo", reason="Accepted risk", waived_by="bob",
        )
        assert waiver.finding_id == "f1"
        assert waiver.active is True

    def test_revoke_waiver(self) -> None:
        em = ExceptionManager()
        w = em.create_waiver("f1", "repo", "r", "a")
        assert em.revoke_waiver(w.id) is True

    def test_is_finding_waived(self) -> None:
        em = ExceptionManager()
        em.create_waiver("f1", "repo", "r", "a")
        assert em.is_finding_waived("f1") is True
        assert em.is_finding_waived("f2") is False

    def test_exception_summary(self) -> None:
        em = ExceptionManager()
        em.create_exception("repo", ExceptionType.SECURITY, "r", "a")
        em.create_exception("repo", ExceptionType.COMPLIANCE, "r", "a")
        summary = em.get_exception_summary("repo")
        assert summary["active"] == 2
