"""Unit tests for EdgeManager."""

from __future__ import annotations

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.edges import EdgeManager
from platform_core.knowledge.types import (
    Node,
    NodeType,
    RelationshipStatus,
    RelationshipType,
)


class TestEdgeManager:
    def _make_managers(self) -> tuple[NodeManager, EdgeManager]:
        store = GraphStore()
        nodes = NodeManager(store)
        edges = EdgeManager(store)
        return nodes, edges

    def test_create_edge(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        e = edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        assert e.source_id == n1.id
        assert e.target_id == n2.id

    def test_get_edge(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        e = edges.create_edge(n1.id, n2.id, RelationshipType.USES)
        fetched = edges.get_edge(e.id)
        assert fetched.relationship_type == RelationshipType.USES

    def test_update_edge(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        e = edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        updated = edges.update_edge(e.id, confidence=0.5)
        assert updated.confidence == 0.5

    def test_update_edge_status(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        e = edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        updated = edges.update_edge(e.id, status=RelationshipStatus.DEPRECATED)
        assert updated.status == RelationshipStatus.DEPRECATED

    def test_delete_edge(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        e = edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        assert edges.delete_edge(e.id) is True
        assert edges.count() == 0

    def test_list_edges_by_source(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        n3 = nodes.create_node(NodeType.MODULE, "c")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        edges.create_edge(n3.id, n2.id, RelationshipType.USES)
        from_source = edges.list_edges(source_id=n1.id)
        assert len(from_source) == 1

    def test_list_edges_by_type(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        edges.create_edge(n1.id, n2.id, RelationshipType.USES)
        deps = edges.list_edges(relationship_type=RelationshipType.DEPENDS_ON)
        assert len(deps) == 1

    def test_get_outgoing(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        outgoing = edges.get_outgoing(n1.id)
        assert len(outgoing) == 1

    def test_get_incoming(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        incoming = edges.get_incoming(n2.id)
        assert len(incoming) == 1

    def test_get_neighbors(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        n3 = nodes.create_node(NodeType.MODULE, "c")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        edges.create_edge(n1.id, n3.id, RelationshipType.USES)
        neighbors = edges.get_neighbors(n1.id)
        assert len(neighbors) == 2

    def test_get_edges_between(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        edges.create_edge(n1.id, n2.id, RelationshipType.USES)
        between = edges.get_edges_between(n1.id, n2.id)
        assert len(between) == 2

    def test_count(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        assert edges.count() == 1

    def test_clear(self) -> None:
        nodes, edges = self._make_managers()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        edges.clear()
        assert edges.count() == 0
