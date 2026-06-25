"""Unit tests for ArchitectureIntelligence."""

from __future__ import annotations

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.edges import EdgeManager
from platform_core.knowledge.architecture import ArchitectureIntelligence
from platform_core.knowledge.types import (
    NodeType,
    RelationshipType,
)


class TestArchitectureIntelligence:
    def _setup(self) -> tuple[NodeManager, EdgeManager, ArchitectureIntelligence]:
        store = GraphStore()
        nodes = NodeManager(store)
        edges = EdgeManager(store)
        intel = ArchitectureIntelligence(store)
        return nodes, edges, intel

    def test_no_smells_on_empty_graph(self) -> None:
        _, _, intel = self._setup()
        smells = intel.detect_smells()
        assert len(smells) == 0

    def test_orphan_service_detected(self) -> None:
        nodes, _, intel = self._setup()
        nodes.create_node(NodeType.SERVICE, "orphan-svc")
        smells = intel.detect_smells()
        orphan = [s for s in smells if s.smell_type == "orphan_service"]
        assert len(orphan) == 1

    def test_no_orphan_when_connected(self) -> None:
        nodes, edges, intel = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "m1")
        svc = nodes.create_node(NodeType.SERVICE, "connected-svc")
        edges.create_edge(n1.id, svc.id, RelationshipType.USES)
        smells = intel.detect_smells()
        orphan = [s for s in smells if s.smell_type == "orphan_service"]
        assert len(orphan) == 0

    def test_dead_module_detected(self) -> None:
        nodes, _, intel = self._setup()
        nodes.create_node(NodeType.MODULE, "dead-mod")
        smells = intel.detect_smells()
        dead = [s for s in smells if s.smell_type == "dead_module"]
        assert len(dead) == 1

    def test_unused_api_detected(self) -> None:
        nodes, _, intel = self._setup()
        nodes.create_node(NodeType.API, "unused-api")
        smells = intel.detect_smells()
        unused = [s for s in smells if s.smell_type == "unused_api"]
        assert len(unused) == 1

    def test_duplicate_services_detected(self) -> None:
        nodes, _, intel = self._setup()
        nodes.create_node(NodeType.SERVICE, "auth")
        nodes.create_node(NodeType.SERVICE, "auth")
        smells = intel.detect_smells()
        dup = [s for s in smells if s.smell_type == "duplicate_service"]
        assert len(dup) == 1

    def test_circular_dependency_detected(self) -> None:
        nodes, edges, intel = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "a")
        n2 = nodes.create_node(NodeType.MODULE, "b")
        edges.create_edge(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        edges.create_edge(n2.id, n1.id, RelationshipType.DEPENDS_ON)
        smells = intel.detect_smells()
        circular = [s for s in smells if s.smell_type == "circular_dependency"]
        assert len(circular) > 0

    def test_high_coupling_detected(self) -> None:
        nodes, edges, intel = self._setup()
        center = nodes.create_node(NodeType.MODULE, "hub")
        for i in range(16):
            other = nodes.create_node(NodeType.MODULE, f"node{i}")
            edges.create_edge(center.id, other.id, RelationshipType.USES)
        smells = intel.detect_smells()
        coupling = [s for s in smells if s.smell_type == "high_coupling"]
        assert len(coupling) == 1

    def test_god_module_detected(self) -> None:
        nodes, edges, intel = self._setup()
        god = nodes.create_node(NodeType.MODULE, "god-mod")
        for i in range(21):
            other = nodes.create_node(NodeType.MODULE, f"dep{i}")
            edges.create_edge(god.id, other.id, RelationshipType.DEPENDS_ON)
        smells = intel.detect_smells()
        god_smells = [s for s in smells if s.smell_type == "god_module"]
        assert len(god_smells) == 1

    def test_generate_recommendations(self) -> None:
        nodes, _, intel = self._setup()
        nodes.create_node(NodeType.SERVICE, "orphan1")
        nodes.create_node(NodeType.SERVICE, "orphan2")
        recs = intel.generate_recommendations()
        assert len(recs) > 0
        assert any("orphan" in r.title.lower() for r in recs)

    def test_architecture_summary(self) -> None:
        nodes, _, intel = self._setup()
        nodes.create_node(NodeType.SERVICE, "orphan")
        summary = intel.get_architecture_summary()
        assert "total_smells" in summary
        assert "by_type" in summary
        assert "by_severity" in summary
        assert summary["total_smells"] >= 1

    def test_empty_graph_recommendations(self) -> None:
        _, _, intel = self._setup()
        recs = intel.generate_recommendations()
        assert len(recs) == 0
