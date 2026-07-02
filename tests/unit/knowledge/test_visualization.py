"""Unit tests for VisualizationEngine."""

from __future__ import annotations

from platform_core.knowledge.edges import EdgeManager
from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.types import NodeType, RelationshipType
from platform_core.knowledge.visualization import VisualizationEngine


class TestVisualizationEngine:
    def _setup(self) -> tuple[NodeManager, EdgeManager, VisualizationEngine]:
        store = GraphStore()
        nodes = NodeManager(store)
        edges = EdgeManager(store)
        viz = VisualizationEngine(store)
        return nodes, edges, viz

    def test_architecture_graph(self) -> None:
        nodes, _, viz = self._setup()
        nodes.create_node(NodeType.MODULE, "m1")
        nodes.create_node(NodeType.SERVICE, "s1")
        vis = viz.generate_architecture_graph()
        assert vis.graph_type == "architecture"
        assert len(vis.nodes) == 2
        assert vis.layout == "force_directed"

    def test_repository_graph(self) -> None:
        nodes, _, viz = self._setup()
        nodes.create_node(NodeType.REPOSITORY, "repo1")
        nodes.create_node(NodeType.MODULE, "m1")
        vis = viz.generate_repository_graph()
        assert vis.graph_type == "repository"
        assert len(vis.nodes) == 1

    def test_dependency_graph(self) -> None:
        nodes, edges, viz = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        vis = viz.generate_dependency_graph()
        assert vis.graph_type == "dependency"
        assert len(vis.nodes) == 2
        assert len(vis.edges) == 1

    def test_dependency_graph_with_root(self) -> None:
        nodes, edges, viz = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "root")
        n2 = nodes.create_node(NodeType.MODULE, "child")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        vis = viz.generate_dependency_graph(n1.id)
        assert vis.graph_type == "dependency"

    def test_service_graph(self) -> None:
        nodes, _, viz = self._setup()
        nodes.create_node(NodeType.SERVICE, "svc1")
        nodes.create_node(NodeType.MODULE, "m1")
        vis = viz.generate_service_graph()
        assert vis.graph_type == "service"
        assert len(vis.nodes) == 1

    def test_module_graph(self) -> None:
        nodes, edges, viz = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        vis = viz.generate_module_graph()
        assert vis.graph_type == "module"
        assert len(vis.nodes) == 2
        assert len(vis.edges) == 1

    def test_event_graph(self) -> None:
        nodes, _, viz = self._setup()
        nodes.create_node(NodeType.EVENT, "evt1")
        vis = viz.generate_event_graph()
        assert vis.graph_type == "event"
        assert len(vis.nodes) == 1

    def test_healthcare_graph(self) -> None:
        nodes, _, viz = self._setup()
        nodes.create_node(NodeType.HEALTHCARE_STANDARD, "FHIR")
        nodes.create_node(NodeType.DEVICE, "analyzer")
        vis = viz.generate_healthcare_graph()
        assert vis.graph_type == "healthcare"
        assert len(vis.nodes) == 2

    def test_device_graph(self) -> None:
        nodes, _, viz = self._setup()
        nodes.create_node(NodeType.DEVICE, "device1")
        nodes.create_node(NodeType.MODULE, "m1")
        vis = viz.generate_device_graph()
        assert vis.graph_type == "device"
        assert len(vis.nodes) == 1

    def test_governance_graph(self) -> None:
        nodes, edges, viz = self._setup()
        svc = nodes.create_node(NodeType.SERVICE, "svc")
        policy = nodes.create_node(NodeType.POLICY, "policy")
        edges.create_edge(svc.id, policy.id, RelationshipType.GOVERNED_BY)
        vis = viz.generate_governance_graph()
        assert vis.graph_type == "governance"
        assert len(vis.nodes) >= 2

    def test_knowledge_timeline(self) -> None:
        nodes, _, viz = self._setup()
        nodes.create_node(NodeType.MODULE, "m1")
        nodes.create_node(NodeType.MODULE, "m2")
        vis = viz.generate_knowledge_timeline()
        assert vis.graph_type == "timeline"
        assert len(vis.nodes) == 2
        assert vis.edges == []

    def test_generate_visualization_dispatch(self) -> None:
        nodes, _, viz = self._setup()
        nodes.create_node(NodeType.MODULE, "m1")
        vis = viz.generate_visualization("service")
        assert vis.graph_type == "service"

    def test_generate_visualization_unknown(self) -> None:
        _, _, viz = self._setup()
        vis = viz.generate_visualization("nonexistent")
        assert vis.graph_type == "unknown"

    def test_empty_graph(self) -> None:
        _, _, viz = self._setup()
        vis = viz.generate_architecture_graph()
        assert len(vis.nodes) == 0
        assert len(vis.edges) == 0

    def test_to_dict(self) -> None:
        nodes, _, viz = self._setup()
        nodes.create_node(NodeType.MODULE, "m1")
        vis = viz.generate_architecture_graph()
        d = vis.to_dict()
        assert "id" in d
        assert "nodes" in d
        assert "edges" in d
        assert d["graph_type"] == "architecture"
