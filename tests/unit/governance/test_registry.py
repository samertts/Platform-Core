"""Unit tests for Governance Registry."""

import pytest

from platform_core.governance.registry import GovernanceRegistry


class TestGovernanceRegistry:
    def test_init(self) -> None:
        gr = GovernanceRegistry()
        assert gr.count() == 0

    def test_record(self) -> None:
        gr = GovernanceRegistry()
        rec = gr.record("review", "repo", "started", actor="alice")
        assert rec.record_type == "review"
        assert rec.actor == "alice"

    def test_get_record(self) -> None:
        gr = GovernanceRegistry()
        rec = gr.record("decision", "repo", "approved")
        found = gr.get_record(rec.id)
        assert found is not None

    def test_list_records(self) -> None:
        gr = GovernanceRegistry()
        gr.record("review", "repo-a", "started")
        gr.record("decision", "repo-b", "approved")
        assert len(gr.list_records()) == 2
        assert len(gr.list_records(repository="repo-a")) == 1

    def test_get_repository_history(self) -> None:
        gr = GovernanceRegistry()
        gr.record("review", "repo", "started")
        gr.record("decision", "repo", "approved")
        history = gr.get_repository_history("repo")
        assert len(history) == 2

    def test_get_statistics(self) -> None:
        gr = GovernanceRegistry()
        gr.record("review", "repo", "started", actor="alice")
        gr.record("decision", "repo", "approved", actor="bob")
        stats = gr.get_statistics()
        assert stats["total_records"] == 2

    def test_clear(self) -> None:
        gr = GovernanceRegistry()
        gr.record("test", "repo", "action")
        gr.clear()
        assert gr.count() == 0
