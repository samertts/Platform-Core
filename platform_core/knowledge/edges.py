"""Edge Manager - Manages knowledge graph relationships.

Handles edge CRUD, relationship queries, and traversal.
"""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import Edge, RelationshipStatus, RelationshipType


class EdgeManager:
    """Manages knowledge graph edges/relationships."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._lock = threading.RLock()

    def create_edge(
        self,
        source_id: str,
        target_id: str,
        relationship_type: RelationshipType,
        version: str = "1.0.0",
        confidence: float = 1.0,
        source_origin: str = "",
        evidence: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Edge:
        edge = Edge(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            version=version,
            confidence=confidence,
            source_origin=source_origin,
            evidence=evidence or [],
            metadata=metadata or {},
        )
        return self._store.add_edge(edge)

    def get_edge(self, edge_id: str) -> Edge:
        return self._store.get_edge(edge_id)

    def update_edge(
        self,
        edge_id: str,
        status: RelationshipStatus | None = None,
        confidence: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Edge:
        edge = self._store.get_edge(edge_id)
        if status is not None:
            edge.status = status
        if confidence is not None:
            edge.confidence = confidence
        if metadata is not None:
            edge.metadata.update(metadata)
        edge.updated_at = datetime.now(UTC)
        return self._store.update_edge(edge)

    def delete_edge(self, edge_id: str) -> bool:
        return self._store.delete_edge(edge_id)

    def list_edges(
        self,
        source_id: str | None = None,
        target_id: str | None = None,
        relationship_type: RelationshipType | None = None,
        status: RelationshipStatus | None = None,
    ) -> list[Edge]:
        edges = self._store.get_all_edges()
        if source_id is not None:
            edges = [e for e in edges if e.source_id == source_id]
        if target_id is not None:
            edges = [e for e in edges if e.target_id == target_id]
        if relationship_type is not None:
            edges = [e for e in edges if e.relationship_type == relationship_type]
        if status is not None:
            edges = [e for e in edges if e.status == status]
        return edges

    def get_outgoing(self, node_id: str) -> list[Edge]:
        return self._store.get_outgoing_edges(node_id)

    def get_incoming(self, node_id: str) -> list[Edge]:
        return self._store.get_incoming_edges(node_id)

    def get_neighbors(self, node_id: str) -> list[str]:
        outgoing = self._store.get_outgoing_edges(node_id)
        incoming = self._store.get_incoming_edges(node_id)
        neighbors = set()
        for e in outgoing:
            neighbors.add(e.target_id)
        for e in incoming:
            neighbors.add(e.source_id)
        return list(neighbors)

    def get_edges_between(self, source_id: str, target_id: str) -> list[Edge]:
        return [e for e in self._store.get_outgoing_edges(source_id) if e.target_id == target_id]

    def count(self) -> int:
        return self._store.edge_count()

    def clear(self) -> None:
        for edge in self._store.get_all_edges():
            self._store.delete_edge(edge.id)
