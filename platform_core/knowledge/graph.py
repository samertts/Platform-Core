"""Graph Store - In-memory graph with adjacency list representation.

Thread-safe graph storage for nodes and edges.
"""

from __future__ import annotations

import threading
from typing import Any

from platform_core.knowledge.types import (
    Edge,
    EdgeNotFoundError,
    GraphConstraintError,
    Node,
    NodeNotFoundError,
)


class GraphStore:
    """In-memory graph store using adjacency lists.

    Provides O(1) node lookup and efficient edge traversal.
    All operations are thread-safe.
    """

    def __init__(self, max_nodes: int = 100000, max_edges: int = 500000) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: dict[str, Edge] = {}
        self._outgoing: dict[str, dict[str, str]] = {}  # node_id -> {edge_id: target_id}
        self._incoming: dict[str, dict[str, str]] = {}  # node_id -> {edge_id: source_id}
        self._max_nodes = max_nodes
        self._max_edges = max_edges
        self._lock = threading.RLock()

    def add_node(self, node: Node) -> Node:
        with self._lock:
            if len(self._nodes) >= self._max_nodes:
                raise GraphConstraintError(f"Maximum node limit ({self._max_nodes}) reached")
            self._nodes[node.id] = node
            self._outgoing.setdefault(node.id, {})
            self._incoming.setdefault(node.id, {})
            return node

    def get_node(self, node_id: str) -> Node:
        with self._lock:
            node = self._nodes.get(node_id)
            if node is None:
                raise NodeNotFoundError(f"Node {node_id} not found")
            return node

    def get_node_optional(self, node_id: str) -> Node | None:
        with self._lock:
            return self._nodes.get(node_id)

    def update_node(self, node: Node) -> Node:
        with self._lock:
            if node.id not in self._nodes:
                raise NodeNotFoundError(f"Node {node.id} not found")
            self._nodes[node.id] = node
            return node

    def delete_node(self, node_id: str) -> bool:
        with self._lock:
            if node_id not in self._nodes:
                return False
            edge_ids = set(self._outgoing.get(node_id, {}).keys())
            edge_ids.update(self._incoming.get(node_id, {}).keys())
            for eid in edge_ids:
                self._edges.pop(eid, None)
            for target_edges in self._outgoing.values():
                target_edges.pop(node_id, None)
            for source_edges in self._incoming.values():
                source_edges.pop(node_id, None)
            self._outgoing.pop(node_id, None)
            self._incoming.pop(node_id, None)
            del self._nodes[node_id]
            return True

    def add_edge(self, edge: Edge) -> Edge:
        with self._lock:
            if len(self._edges) >= self._max_edges:
                raise GraphConstraintError(f"Maximum edge limit ({self._max_edges}) reached")
            if edge.source_id not in self._nodes:
                raise NodeNotFoundError(f"Source node {edge.source_id} not found")
            if edge.target_id not in self._nodes:
                raise NodeNotFoundError(f"Target node {edge.target_id} not found")
            self._edges[edge.id] = edge
            self._outgoing.setdefault(edge.source_id, {})[edge.id] = edge.target_id
            self._incoming.setdefault(edge.target_id, {})[edge.id] = edge.source_id
            return edge

    def get_edge(self, edge_id: str) -> Edge:
        with self._lock:
            edge = self._edges.get(edge_id)
            if edge is None:
                raise EdgeNotFoundError(f"Edge {edge_id} not found")
            return edge

    def update_edge(self, edge: Edge) -> Edge:
        with self._lock:
            if edge.id not in self._edges:
                raise EdgeNotFoundError(f"Edge {edge.id} not found")
            old = self._edges[edge.id]
            if old.source_id != edge.source_id or old.target_id != edge.target_id:
                self._outgoing.get(old.source_id, {}).pop(edge.id, None)
                self._incoming.get(old.target_id, {}).pop(edge.id, None)
                self._outgoing.setdefault(edge.source_id, {})[edge.id] = edge.target_id
                self._incoming.setdefault(edge.target_id, {})[edge.id] = edge.source_id
            self._edges[edge.id] = edge
            return edge

    def delete_edge(self, edge_id: str) -> bool:
        with self._lock:
            edge = self._edges.pop(edge_id, None)
            if edge is None:
                return False
            self._outgoing.get(edge.source_id, {}).pop(edge_id, None)
            self._incoming.get(edge.target_id, {}).pop(edge_id, None)
            return True

    def get_outgoing_edges(self, node_id: str) -> list[Edge]:
        with self._lock:
            edge_ids = self._outgoing.get(node_id, {})
            return [self._edges[eid] for eid in edge_ids if eid in self._edges]

    def get_incoming_edges(self, node_id: str) -> list[Edge]:
        with self._lock:
            edge_ids = self._incoming.get(node_id, {})
            return [self._edges[eid] for eid in edge_ids if eid in self._edges]

    def get_neighbors(self, node_id: str) -> list[Node]:
        with self._lock:
            target_ids = self._outgoing.get(node_id, {}).values()
            return [self._nodes[tid] for tid in target_ids if tid in self._nodes]

    def get_all_nodes(self) -> list[Node]:
        with self._lock:
            return list(self._nodes.values())

    def get_all_edges(self) -> list[Edge]:
        with self._lock:
            return list(self._edges.values())

    def get_nodes_by_type(self, node_type: Any) -> list[Node]:
        with self._lock:
            return [n for n in self._nodes.values() if n.node_type == node_type]

    def get_edges_by_type(self, rel_type: Any) -> list[Edge]:
        with self._lock:
            return [e for e in self._edges.values() if e.relationship_type == rel_type]

    def node_count(self) -> int:
        with self._lock:
            return len(self._nodes)

    def edge_count(self) -> int:
        with self._lock:
            return len(self._edges)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "nodes": {nid: n.to_dict() for nid, n in self._nodes.items()},
                "edges": {eid: e.to_dict() for eid, e in self._edges.items()},
                "node_count": len(self._nodes),
                "edge_count": len(self._edges),
            }

    def clear(self) -> None:
        with self._lock:
            self._nodes.clear()
            self._edges.clear()
            self._outgoing.clear()
            self._incoming.clear()
