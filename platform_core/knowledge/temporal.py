"""Temporal Graph Manager - Manages historical evolution of the graph.

Provides snapshot creation, restoration, and temporal queries.
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import (Edge, EventType, GraphSnapshot,
                                           Node, TemporalError, TemporalEvent)


class TemporalManager:
    """Manages temporal history of the knowledge graph."""

    def __init__(self, store: GraphStore, max_history: int = 10000) -> None:
        self._store = store
        self._events: list[TemporalEvent] = []
        self._snapshots: list[GraphSnapshot] = []
        self._max_history = max_history
        self._lock = threading.RLock()

    def record_event(
        self,
        event_type: EventType,
        entity_id: str,
        entity_type: Any = None,
        old_value: dict[str, Any] | None = None,
        new_value: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> TemporalEvent:
        event = TemporalEvent(
            event_type=event_type,
            entity_id=entity_id,
            entity_type=entity_type,
            old_value=old_value,
            new_value=new_value,
            metadata=metadata or {},
        )
        with self._lock:
            self._events.append(event)
            if len(self._events) > self._max_history:
                self._events = self._events[-self._max_history :]
        return event

    def create_snapshot(self, description: str = "") -> GraphSnapshot:
        data = self._store.snapshot()
        snapshot = GraphSnapshot(
            description=description,
            node_count=data["node_count"],
            edge_count=data["edge_count"],
            nodes_snapshot=data["nodes"],
            edges_snapshot=data["edges"],
        )
        with self._lock:
            self._snapshots.append(snapshot)
        self.record_event(
            EventType.SNAPSHOT_CREATED,
            snapshot.id,
            metadata={"description": description, "node_count": data["node_count"]},
        )
        return snapshot

    def restore_snapshot(self, snapshot_id: str) -> bool:
        with self._lock:
            snapshot = None
            for s in self._snapshots:
                if s.id == snapshot_id:
                    snapshot = s
                    break
            if snapshot is None:
                return False
        self._store.clear()
        for node_id, node_data in snapshot.nodes_snapshot.items():
            node = Node(
                id=node_id,
                name=node_data.get("name", ""),
                metadata=node_data.get("metadata", {}),
            )
            node.node_type = node_data.get("node_type", "module")
            node.status = node_data.get("status", "active")
            node.lifecycle = node_data.get("lifecycle", "development")
            node.version = node_data.get("version", "1.0.0")
            node.owner = node_data.get("owner", "")
            node.labels = node_data.get("labels", [])
            node.tags = node_data.get("tags", [])
            node.capabilities = node_data.get("capabilities", [])
            self._store.add_node(node)
        for edge_id, edge_data in snapshot.edges_snapshot.items():
            edge = Edge(
                id=edge_id,
                source_id=edge_data.get("source_id", ""),
                target_id=edge_data.get("target_id", ""),
            )
            edge.relationship_type = edge_data.get("relationship_type", "depends_on")
            edge.status = edge_data.get("status", "active")
            edge.version = edge_data.get("version", "1.0.0")
            edge.confidence = edge_data.get("confidence", 1.0)
            edge.source_origin = edge_data.get("source_origin", "")
            edge.evidence = edge_data.get("evidence", [])
            edge.metadata = edge_data.get("metadata", {})
            self._store.add_edge(edge)
        self.record_event(
            EventType.SNAPSHOT_RESTORED,
            snapshot_id,
            metadata={"description": snapshot.description},
        )
        return True

    def get_events(
        self,
        entity_id: str | None = None,
        event_type: EventType | None = None,
        since: datetime | None = None,
        limit: int = 100,
    ) -> list[TemporalEvent]:
        with self._lock:
            events = list(self._events)
        if entity_id is not None:
            events = [e for e in events if e.entity_id == entity_id]
        if event_type is not None:
            events = [e for e in events if e.event_type == event_type]
        if since is not None:
            events = [e for e in events if e.timestamp >= since]
        return events[-limit:]

    def get_snapshots(self, limit: int = 50) -> list[GraphSnapshot]:
        with self._lock:
            return list(self._snapshots)[-limit:]

    def get_snapshot(self, snapshot_id: str) -> GraphSnapshot | None:
        with self._lock:
            for s in self._snapshots:
                if s.id == snapshot_id:
                    return s
        return None

    def get_entity_history(self, entity_id: str) -> list[TemporalEvent]:
        with self._lock:
            return [e for e in self._events if e.entity_id == entity_id]

    def get_latest_snapshot(self) -> GraphSnapshot | None:
        with self._lock:
            return self._snapshots[-1] if self._snapshots else None

    def event_count(self) -> int:
        with self._lock:
            return len(self._events)

    def snapshot_count(self) -> int:
        with self._lock:
            return len(self._snapshots)

    def clear(self) -> None:
        with self._lock:
            self._events.clear()
            self._snapshots.clear()
