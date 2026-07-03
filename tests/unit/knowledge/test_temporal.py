"""Unit tests for TemporalManager."""

from __future__ import annotations

from platform_core.knowledge.edges import EdgeManager
from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.temporal import TemporalManager
from platform_core.knowledge.types import EventType, NodeType


class TestTemporalManager:
    def _make_managers(self) -> tuple[NodeManager, EdgeManager, TemporalManager]:
        store = GraphStore()
        nodes = NodeManager(store)
        edges = EdgeManager(store)
        temporal = TemporalManager(store)
        return nodes, edges, temporal

    def test_record_event(self) -> None:
        _, _, temporal = self._make_managers()
        event = temporal.record_event(EventType.NODE_CREATED, "n1")
        assert event.event_type == EventType.NODE_CREATED
        assert event.entity_id == "n1"

    def test_event_count(self) -> None:
        _, _, temporal = self._make_managers()
        temporal.record_event(EventType.NODE_CREATED, "n1")
        temporal.record_event(EventType.NODE_UPDATED, "n1")
        assert temporal.event_count() == 2

    def test_create_snapshot(self) -> None:
        nodes, _, temporal = self._make_managers()
        nodes.create_node(NodeType.MODULE, "m1")
        snap = temporal.create_snapshot("test snapshot")
        assert snap.description == "test snapshot"
        assert snap.node_count == 1

    def test_snapshot_count(self) -> None:
        _, _, temporal = self._make_managers()
        temporal.create_snapshot("s1")
        temporal.create_snapshot("s2")
        assert temporal.snapshot_count() == 2

    def test_get_snapshots(self) -> None:
        _, _, temporal = self._make_managers()
        temporal.create_snapshot("s1")
        temporal.create_snapshot("s2")
        snaps = temporal.get_snapshots()
        assert len(snaps) == 2

    def test_get_snapshot_by_id(self) -> None:
        _, _, temporal = self._make_managers()
        snap = temporal.create_snapshot("s1")
        fetched = temporal.get_snapshot(snap.id)
        assert fetched is not None
        assert fetched.description == "s1"

    def test_get_snapshot_not_found(self) -> None:
        _, _, temporal = self._make_managers()
        assert temporal.get_snapshot("nonexistent") is None

    def test_restore_snapshot(self) -> None:
        nodes, _, temporal = self._make_managers()
        nodes.create_node(NodeType.MODULE, "m1")
        snap = temporal.create_snapshot("before")
        nodes.create_node(NodeType.MODULE, "m2")
        assert nodes.count() == 2
        restored = temporal.restore_snapshot(snap.id)
        assert restored is True
        assert nodes.count() == 1

    def test_restore_snapshot_not_found(self) -> None:
        _, _, temporal = self._make_managers()
        assert temporal.restore_snapshot("nonexistent") is False

    def test_get_latest_snapshot(self) -> None:
        _, _, temporal = self._make_managers()
        temporal.create_snapshot("first")
        temporal.create_snapshot("second")
        latest = temporal.get_latest_snapshot()
        assert latest is not None
        assert latest.description == "second"

    def test_get_latest_snapshot_empty(self) -> None:
        _, _, temporal = self._make_managers()
        assert temporal.get_latest_snapshot() is None

    def test_get_events_filtered(self) -> None:
        _, _, temporal = self._make_managers()
        temporal.record_event(EventType.NODE_CREATED, "n1")
        temporal.record_event(EventType.NODE_UPDATED, "n1")
        temporal.record_event(EventType.NODE_CREATED, "n2")
        created = temporal.get_events(event_type=EventType.NODE_CREATED)
        assert len(created) == 2
        n1_events = temporal.get_events(entity_id="n1")
        assert len(n1_events) == 2

    def test_get_entity_history(self) -> None:
        _, _, temporal = self._make_managers()
        temporal.record_event(EventType.NODE_CREATED, "n1")
        temporal.record_event(EventType.NODE_CREATED, "n2")
        history = temporal.get_entity_history("n1")
        assert len(history) == 1

    def test_clear(self) -> None:
        _, _, temporal = self._make_managers()
        temporal.record_event(EventType.NODE_CREATED, "n1")
        temporal.create_snapshot("s1")
        temporal.clear()
        assert temporal.event_count() == 0
        assert temporal.snapshot_count() == 0
