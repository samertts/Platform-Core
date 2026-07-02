"""Unit tests for QueryEngine."""

from __future__ import annotations

from platform_core.knowledge.edges import EdgeManager
from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.queries import QueryEngine
from platform_core.knowledge.types import NodeType, QueryType, RelationshipType


class TestQueryEngine:
    def _setup(self) -> tuple[GraphStore, NodeManager, EdgeManager, QueryEngine]:
        store = GraphStore()
        nodes = NodeManager(store)
        edges = EdgeManager(store)
        queries = QueryEngine(store)
        return store, nodes, edges, queries

    def test_dependency_analysis(self) -> None:
        _, nodes, edges, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        n3 = nodes.create_node(NodeType.MODULE, "c")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        edges.create_edge(n2.id, n3.id, RelationshipType.DEPENDS_ON)
        result = queries.dependency_analysis(n1.id)
        assert len(result.nodes) >= 2
        assert len(result.edges) >= 1
        assert result.query_type == QueryType.DEPENDENCY_ANALYSIS

    def test_impact_analysis(self) -> None:
        _, nodes, edges, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        n3 = nodes.create_node(NodeType.MODULE, "c")
        edges.create_edge(n2.id, n1.id, RelationshipType.DEPENDS_ON)
        edges.create_edge(n3.id, n1.id, RelationshipType.DEPENDS_ON)
        result = queries.impact_analysis(n1.id)
        assert len(result.nodes) >= 2
        assert result.query_type == QueryType.IMPACT_ANALYSIS

    def test_circular_dependency_none(self) -> None:
        _, nodes, edges, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        result = queries.circular_dependency()
        assert len(result.paths) == 0

    def test_circular_dependency_detected(self) -> None:
        _, nodes, edges, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        edges.create_edge(n2.id, n1.id, RelationshipType.DEPENDS_ON)
        result = queries.circular_dependency()
        assert len(result.paths) > 0

    def test_shortest_path_found(self) -> None:
        _, nodes, edges, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        n3 = nodes.create_node(NodeType.MODULE, "c")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        edges.create_edge(n2.id, n3.id, RelationshipType.DEPENDS_ON)
        result = queries.shortest_path(n1.id, n3.id)
        assert result.metadata.get("found") is True
        assert len(result.paths) == 1

    def test_shortest_path_same_node(self) -> None:
        _, nodes, _, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        result = queries.shortest_path(n1.id, n1.id)
        assert result.metadata.get("found") is True
        assert result.paths == [[n1.id]]

    def test_shortest_path_not_found(self) -> None:
        _, nodes, edges, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        result = queries.shortest_path(n1.id, n2.id)
        assert result.metadata.get("found") is False

    def test_reachability(self) -> None:
        _, nodes, edges, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        result = queries.reachability(n1.id, n2.id)
        assert result.metadata.get("reachable") is True
        assert result.query_type == QueryType.REACHABILITY

    def test_architecture_navigation(self) -> None:
        _, nodes, edges, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "center")
        n2 = nodes.create_node(NodeType.MODULE, "neighbor")
        edges.create_edge(n1.id, n2.id, RelationshipType.USES)
        result = queries.architecture_navigation(n1.id)
        assert len(result.nodes) >= 2
        assert result.query_type == QueryType.ARCHITECTURE_NAVIGATION

    def test_repository_health(self) -> None:
        store, nodes, _, queries = self._setup()
        nodes.create_node(NodeType.REPOSITORY, "repo1")
        nodes.create_node(NodeType.MODULE, "mod1")
        result = queries.repository_health()
        assert len(result.nodes) == 1
        assert result.query_type == QueryType.REPOSITORY_HEALTH

    def test_execute_query_dispatch(self) -> None:
        _, nodes, edges, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        result = queries.execute_query(QueryType.DEPENDENCY_ANALYSIS, n1.id)
        assert result.query_type == QueryType.DEPENDENCY_ANALYSIS

    def test_execute_query_records_time(self) -> None:
        _, nodes, _, queries = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        result = queries.execute_query(QueryType.DEPENDENCY_ANALYSIS, n1.id)
        assert result.execution_time_ms >= 0.0
