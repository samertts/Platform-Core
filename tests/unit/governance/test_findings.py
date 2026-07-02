"""Unit tests for Finding Manager."""

import pytest

from platform_core.governance.findings import FindingManager
from platform_core.governance.types import FindingSeverity, FindingStatus


class TestFindingManager:
    def test_init(self) -> None:
        fm = FindingManager()
        assert fm.count() == 0

    def test_create_finding(self) -> None:
        fm = FindingManager()
        f = fm.create_finding(
            repository="repo",
            severity=FindingSeverity.CRITICAL,
            category="security",
            title="test",
            description="desc",
        )
        assert f.repository == "repo"
        assert f.severity == FindingSeverity.CRITICAL
        assert f.status == FindingStatus.OPEN

    def test_get_finding(self) -> None:
        fm = FindingManager()
        f = fm.create_finding("repo", FindingSeverity.HIGH, "test", "t", "d")
        found = fm.get_finding(f.id)
        assert found is not None
        assert found.id == f.id

    def test_get_finding_not_found(self) -> None:
        fm = FindingManager()
        assert fm.get_finding("nonexistent") is None

    def test_update_status(self) -> None:
        fm = FindingManager()
        f = fm.create_finding("repo", FindingSeverity.MEDIUM, "test", "t", "d")
        updated = fm.update_status(f.id, FindingStatus.RESOLVED)
        assert updated is not None
        assert updated.status == FindingStatus.RESOLVED
        assert updated.resolved_at is not None

    def test_update_status_not_found(self) -> None:
        fm = FindingManager()
        assert fm.update_status("nonexistent", FindingStatus.RESOLVED) is None

    def test_update_finding(self) -> None:
        fm = FindingManager()
        f = fm.create_finding("repo", FindingSeverity.LOW, "test", "t", "d")
        updated = fm.update_finding(f.id, owner="alice")
        assert updated is not None
        assert updated.owner == "alice"

    def test_delete_finding(self) -> None:
        fm = FindingManager()
        f = fm.create_finding("repo", FindingSeverity.INFO, "test", "t", "d")
        assert fm.delete_finding(f.id) is True
        assert fm.get_finding(f.id) is None

    def test_delete_not_found(self) -> None:
        fm = FindingManager()
        assert fm.delete_finding("nonexistent") is False

    def test_list_findings(self) -> None:
        fm = FindingManager()
        fm.create_finding("repo-a", FindingSeverity.CRITICAL, "s", "t", "d")
        fm.create_finding("repo-b", FindingSeverity.HIGH, "t", "t", "d")
        fm.create_finding("repo-a", FindingSeverity.LOW, "s", "t", "d")

        assert len(fm.list_findings()) == 3
        assert len(fm.list_findings(repository="repo-a")) == 2
        assert len(fm.list_findings(severity=FindingSeverity.CRITICAL)) == 1

    def test_get_findings_summary(self) -> None:
        fm = FindingManager()
        fm.create_finding("repo", FindingSeverity.CRITICAL, "s", "t", "d")
        fm.create_finding("repo", FindingSeverity.HIGH, "t", "t", "d")
        summary = fm.get_findings_summary("repo")
        assert summary["total"] == 2
        assert summary["critical_count"] == 1

    def test_get_critical_findings(self) -> None:
        fm = FindingManager()
        fm.create_finding("repo", FindingSeverity.CRITICAL, "s", "t", "d")
        fm.create_finding("repo", FindingSeverity.HIGH, "t", "t", "d")
        critical = fm.get_critical_findings("repo")
        assert len(critical) == 1

    def test_has_blocking_findings(self) -> None:
        fm = FindingManager()
        fm.create_finding("repo", FindingSeverity.CRITICAL, "s", "t", "d")
        assert fm.has_blocking_findings("repo") is True

    def test_no_blocking_findings(self) -> None:
        fm = FindingManager()
        fm.create_finding("repo", FindingSeverity.LOW, "s", "t", "d")
        assert fm.has_blocking_findings("repo") is False

    def test_clear(self) -> None:
        fm = FindingManager()
        fm.create_finding("repo", FindingSeverity.HIGH, "s", "t", "d")
        fm.clear()
        assert fm.count() == 0
