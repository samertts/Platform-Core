"""Unit tests for GraphStore."""

from __future__ import annotations

import pytest
from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import (
    Edge,
    GraphConstraintError,
    Node,
    NodeNotFoundError,
    NodeType,
    RelationshipType,
    EdgeNotFoundError,
)


class TestGraphStore:
    def test_init(self) -> None:
        store = GraphStore()
        assert store.node_count() == 0
        assert store.edge_count() == 0

    def test_add_and_get_node(self) -> None:
        store = GraphStore()
        node = Node(name="test", node_type=NodeType.MODULE)
        store.add_node(node)
        result = store.get_node(node.id)
        assert result.name == "test"

    def test_get_node_not_found(self) -> None:
        store = GraphStore()
        with pytest.raises(NodeNotFoundError):
            store.get_node("nonexistent")

    def test_get_node_optional(self) -> None:
        store = GraphStore()
        assert store.get_node_optional("nonexistent") is None
        node = Node(name="a")
        store.add_node(node)
        assert store.get_node_optional(node.id) is not None

    def test_update_node(self) -> None:
        store = GraphStore()
        node = Node(name="old")
        store.add_node(node)
        node.name = "new"
        store.update_node(node)
        assert store.get_node(node.id).name == "new"

    def test_update_node_not_found(self) -> None:
        store = GraphStore()
        node = Node(name="ghost")
        with pytest.raises(NodeNotFoundError):
            store.update_node(node)

    def test_delete_node(self) -> None:
        store = GraphStore()
        node = Node(name="del")
        store.add_node(node)
        assert store.delete_node(node.id) is True
        assert store.get_node_optional(node.id) is None

    def test_delete_node_not_found(self) -> None:
        store = GraphStore()
        assert store.delete_node("nope") is False

    def test_add_edge(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        edge = Edge(source_id=n1.id, target_id=n2.id)
        store.add_edge(edge)
        assert store.get_edge(edge.id).source_id == n1.id

    def test_add_edge_source_not_found(self) -> None:
        store = GraphStore()
        n2 = Node(name="b")
        store.add_node(n2)
        edge = Edge(source_id="ghost", target_id=n2.id)
        with pytest.raises(NodeNotFoundError):
            store.add_edge(edge)

    def test_add_edge_target_not_found(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        store.add_node(n1)
        edge = Edge(source_id=n1.id, target_id="ghost")
        with pytest.raises(NodeNotFoundError):
            store.add_edge(edge)

    def test_delete_edge(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        edge = Edge(source_id=n1.id, target_id=n2.id)
        store.add_edge(edge)
        assert store.delete_edge(edge.id) is True
        assert store.edge_count() == 0

    def test_delete_edge_not_found(self) -> None:
        store = GraphStore()
        assert store.delete_edge("nope") is False

    def test_get_outgoing_and_incoming(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        edge = Edge(source_id=n1.id, target_id=n2.id)
        store.add_edge(edge)
        outgoing = store.get_outgoing_edges(n1.id)
        incoming = store.get_incoming_edges(n2.id)
        assert len(outgoing) == 1
        assert len(incoming) == 1

    def test_get_neighbors(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        edge = Edge(source_id=n1.id, target_id=n2.id)
        store.add_edge(edge)
        neighbors = store.get_neighbors(n1.id)
        assert len(neighbors) == 1
        assert neighbors[0].name == "b"

    def test_node_count_and_edge_count(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        assert store.node_count() == 2
        edge = Edge(source_id=n1.id, target_id=n2.id)
        store.add_edge(edge)
        assert store.edge_count() == 1

    def test_get_nodes_by_type(self) -> None:
        store = GraphStore()
        store.add_node(Node(name="m1", node_type=NodeType.MODULE))
        store.add_node(Node(name="s1", node_type=NodeType.SERVICE))
        modules = store.get_nodes_by_type(NodeType.MODULE)
        assert len(modules) == 1
        assert modules[0].name == "m1"

    def test_get_edges_by_type(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        e1 = Edge(source_id=n1.id, target_id=n2.id, relationship_type=RelationshipType.DEPENDS_ON)
        e2 = Edge(source_id=n1.id, target_id=n2.id, relationship_type=RelationshipType.USES)
        store.add_edge(e1)
        store.add_edge(e2)
        deps = store.get_edges_by_type(RelationshipType.DEPENDS_ON)
        assert len(deps) == 1

    def test_snapshot(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        store.add_node(n1)
        snap = store.snapshot()
        assert snap["node_count"] == 1
        assert n1.id in snap["nodes"]

    def test_clear(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        edge = Edge(source_id=n1.id, target_id=n2.id)
        store.add_edge(edge)
        store.clear()
        assert store.node_count() == 0
        assert store.edge_count() == 0

    def test_max_nodes_constraint(self) -> None:
        store = GraphStore(max_nodes=2)
        store.add_node(Node(name="a"))
        store.add_node(Node(name="b"))
        with pytest.raises(GraphConstraintError):
            store.add_node(Node(name="c"))

    def test_max_edges_constraint(self) -> None:
        store = GraphStore(max_edges=1)
        n1 = Node(name="a")
        n2 = Node(name="b")
        n3 = Node(name="c")
        store.add_node(n1)
        store.add_node(n2)
        store.add_node(n3)
        store.add_edge(Edge(source_id=n1.id, target_id=n2.id))
        with pytest.raises(GraphConstraintError):
            store.add_edge(Edge(source_id=n2.id, target_id=n3.id))

    def test_delete_node_removes_edges(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        e = Edge(source_id=n1.id, target_id=n2.id)
        store.add_edge(e)
        store.delete_node(n1.id)
        assert store.edge_count() == 0

    def test_get_all_nodes_and_edges(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        e = Edge(source_id=n1.id, target_id=n2.id)
        store.add_edge(e)
        assert len(store.get_all_nodes()) == 2
        assert len(store.get_all_edges()) == 1

    def test_update_edge(self) -> None:
        store = GraphStore()
        n1 = Node(name="a")
        n2 = Node(name="b")
        store.add_node(n1)
        store.add_node(n2)
        e = Edge(source_id=n1.id, target_id=n2.id)
        store.add_edge(e)
        e.confidence = 0.5
        store.update_edge(e)
        assert store.get_edge(e.id).confidence == 0.5
