"""Unit tests for ImpactAnalyzer."""

from __future__ import annotations

from platform_core.knowledge.edges import EdgeManager
from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.impact import ImpactAnalyzer
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.types import (ChangeType, ImpactLevel, NodeType,
                                           RelationshipType)


class TestImpactAnalyzer:
    def _setup(self) -> tuple[NodeManager, EdgeManager, ImpactAnalyzer]:
        store = GraphStore()
        nodes = NodeManager(store)
        edges = EdgeManager(store)
        analyzer = ImpactAnalyzer(store)
        return nodes, edges, analyzer

    def test_no_impact(self) -> None:
        nodes, _, analyzer = self._setup()
        n = nodes.create_node(NodeType.MODULE, "isolated")
        report = analyzer.analyze_impact(n.id)
        assert report.impact_level == ImpactLevel.NONE
        assert report.total_affected == 0

    def test_low_impact(self) -> None:
        nodes, edges, analyzer = self._setup()
        n1 = nodes.create_node(NodeType.MODULE, "target")
        n2 = nodes.create_node(NodeType.SERVICE, "svc1")
        edges.create_edge(n2.id, n1.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(n1.id)
        assert report.impact_level == ImpactLevel.LOW
        assert report.total_affected == 1

    def test_medium_impact(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        for i in range(5):
            svc = nodes.create_node(NodeType.SERVICE, f"svc{i}")
            edges.create_edge(svc.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert report.total_affected >= 4

    def test_high_impact(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        for i in range(20):
            svc = nodes.create_node(NodeType.SERVICE, f"svc{i}")
            edges.create_edge(svc.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert report.impact_level == ImpactLevel.HIGH

    def test_critical_impact(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        for i in range(30):
            svc = nodes.create_node(NodeType.SERVICE, f"svc{i}")
            edges.create_edge(svc.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert report.impact_level == ImpactLevel.CRITICAL

    def test_categorize_repositories(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        repo = nodes.create_node(NodeType.REPOSITORY, "repo1")
        edges.create_edge(repo.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert "repo1" in report.affected_repositories

    def test_categorize_apis(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        api = nodes.create_node(NodeType.API, "api1")
        edges.create_edge(api.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert "api1" in report.affected_apis

    def test_categorize_events(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        evt = nodes.create_node(NodeType.EVENT, "evt1")
        edges.create_edge(evt.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert "evt1" in report.affected_events

    def test_categorize_workflows(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        wf = nodes.create_node(NodeType.WORKFLOW, "wf1")
        edges.create_edge(wf.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert "wf1" in report.affected_workflows

    def test_categorize_packages(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        pkg = nodes.create_node(NodeType.PACKAGE, "pkg1")
        edges.create_edge(pkg.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert "pkg1" in report.affected_packages

    def test_categorize_deployments(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        dep = nodes.create_node(NodeType.DEPLOYMENT, "dep1")
        edges.create_edge(dep.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert "dep1" in report.affected_deployments

    def test_recommendations_generated(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        for i in range(5):
            svc = nodes.create_node(NodeType.SERVICE, f"svc{i}")
            edges.create_edge(svc.id, target.id, RelationshipType.DEPENDS_ON)
        report = analyzer.analyze_impact(target.id)
        assert len(report.recommendations) > 0

    def test_change_type_modify(self) -> None:
        nodes, edges, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        report = analyzer.analyze_impact(target.id, ChangeType.MODIFY)
        assert report.change_type == ChangeType.MODIFY

    def test_change_type_delete(self) -> None:
        nodes, _, analyzer = self._setup()
        target = nodes.create_node(NodeType.MODULE, "target")
        report = analyzer.analyze_impact(target.id, ChangeType.DELETE)
        assert report.change_type == ChangeType.DELETE
