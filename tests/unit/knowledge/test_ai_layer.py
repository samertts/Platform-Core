"""Unit tests for AIKnowledgeLayer."""

from __future__ import annotations

from platform_core.knowledge.ai_layer import AIKnowledgeLayer
from platform_core.knowledge.edges import EdgeManager
from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.types import NodeType, RelationshipType


class TestAIKnowledgeLayer:
    def _setup(self) -> tuple[NodeManager, EdgeManager, AIKnowledgeLayer]:
        store = GraphStore()
        nodes = NodeManager(store)
        edges = EdgeManager(store)
        ai = AIKnowledgeLayer(store)
        return nodes, edges, ai

    def test_reason_architecture_with_node(self) -> None:
        nodes, _, ai = self._setup()
        n = nodes.create_node(NodeType.SERVICE, "auth")
        result = ai.reason_architecture("describe auth", n.id)
        assert result.reasoning_type == "architecture"
        assert result.confidence > 0
        assert len(result.supporting_nodes) > 0

    def test_reason_architecture_overview(self) -> None:
        nodes, _, ai = self._setup()
        nodes.create_node(NodeType.MODULE, "m1")
        result = ai.reason_architecture("overview")
        assert "nodes" in result.answer
        assert result.confidence > 0

    def test_reason_architecture_recommendations(self) -> None:
        nodes, edges, ai = self._setup()
        svc = nodes.create_node(NodeType.SERVICE, "heavy")
        for i in range(12):
            other = nodes.create_node(NodeType.MODULE, f"dep{i}")
            edges.create_edge(svc.id, other.id, RelationshipType.DEPENDS_ON)
        result = ai.reason_architecture("analyze", svc.id)
        assert len(result.recommendations) > 0

    def test_reason_dependencies(self) -> None:
        nodes, edges, ai = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "core")
        n2 = nodes.create_node(NodeType.MODULE, "util")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        result = ai.reason_dependencies("what does core depend on", n1.id)
        assert result.reasoning_type == "dependencies"
        assert "core" in result.answer

    def test_reason_impact(self) -> None:
        nodes, edges, ai = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        for i in range(5):
            svc = nodes.create_node(NodeType.SERVICE, f"svc{i}")
            edges.create_edge(svc.id, target.id, RelationshipType.DEPENDS_ON)
        result = ai.reason_impact("impact of changing target", target.id)
        assert result.reasoning_type == "impact"
        assert "5" in result.answer

    def test_reason_impact_high(self) -> None:
        nodes, edges, ai = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        for i in range(15):
            svc = nodes.create_node(NodeType.SERVICE, f"svc{i}")
            edges.create_edge(svc.id, target.id, RelationshipType.DEPENDS_ON)
        result = ai.reason_impact("impact", target.id)
        assert len(result.recommendations) > 0

    def test_reason_migration(self) -> None:
        nodes, edges, ai = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "old")
        n2 = nodes.create_node(NodeType.MODULE, "dep")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        n3 = nodes.create_node(NodeType.SERVICE, "user")
        edges.create_edge(n3.id, n1.id, RelationshipType.DEPENDS_ON)
        result = ai.reason_migration("migrate old", n1.id)
        assert result.reasoning_type == "migration"
        assert len(result.recommendations) > 0

    def test_reason_refactoring(self) -> None:
        nodes, edges, ai = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "complex")
        for i in range(12):
            other = nodes.create_node(NodeType.MODULE, f"dep{i}")
            edges.create_edge(n1.id, other.id, RelationshipType.USES)
        result = ai.reason_refactoring("refactor complex", n1.id)
        assert result.reasoning_type == "refactoring"
        assert len(result.recommendations) > 0

    def test_reason_governance(self) -> None:
        nodes, edges, ai = self._setup()
        svc = nodes.create_node(NodeType.SERVICE, "svc")
        policy = nodes.create_node(NodeType.POLICY, "policy1")
        edges.create_edge(policy.id, svc.id, RelationshipType.GOVERNED_BY)
        result = ai.reason_governance("governance of svc", svc.id)
        assert result.reasoning_type == "governance"
        assert "1 governance" in result.answer

    def test_reason_governance_no_cert(self) -> None:
        nodes, _, ai = self._setup()
        svc = nodes.create_node(NodeType.SERVICE, "svc")
        result = ai.reason_governance("governance", svc.id)
        assert len(result.recommendations) > 0

    def test_reason_risk(self) -> None:
        nodes, edges, ai = self._setup()
        svc = nodes.create_node(NodeType.SERVICE, "critical")
        for i in range(8):
            other = nodes.create_node(NodeType.MODULE, f"dep{i}")
            edges.create_edge(svc.id, other.id, RelationshipType.DEPENDS_ON)
        result = ai.reason_risk("risk of critical", svc.id)
        assert result.reasoning_type == "risk"
        assert "score" in result.answer.lower()

    def test_reason_healthcare(self) -> None:
        nodes, _, ai = self._setup()
        node = nodes.create_node(
            NodeType.HEALTHCARE_STANDARD,
            "FHIR",
            labels=["fhir", "hl7"],
        )
        result = ai.reason_healthcare("healthcare analysis", node.id)
        assert result.reasoning_type == "healthcare"
        assert len(result.recommendations) > 0

    def test_ask_dispatch(self) -> None:
        nodes, _, ai = self._setup()
        nodes.create_node(NodeType.MODULE, "m1")
        result = ai.ask("overview", reasoning_type="architecture")
        assert result.reasoning_type == "architecture"

    def test_ask_unknown_type_falls_back(self) -> None:
        nodes, _, ai = self._setup()
        nodes.create_node(NodeType.MODULE, "m1")
        result = ai.ask("overview", reasoning_type="nonexistent")
        assert result.reasoning_type == "architecture"
