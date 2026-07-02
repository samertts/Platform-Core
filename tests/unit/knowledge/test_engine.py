"""Unit tests for KnowledgeEngine."""

from __future__ import annotations

import pytest

from platform_core.knowledge.engine import KnowledgeEngine
from platform_core.knowledge.types import (
    ChangeType,
    EventType,
    HealthcareEntity,
    HealthcareStandard,
    KnowledgeEngineConfig,
    NodeNotFoundError,
    NodeType,
    QueryType,
    RelationshipType,
)


class TestKnowledgeEngine:
    def test_init_default(self) -> None:
        engine = KnowledgeEngine()
        assert engine is not None
        assert engine._config.max_nodes == 100000

    def test_init_custom_config(self) -> None:
        config = KnowledgeEngineConfig(max_nodes=100, max_edges=200)
        engine = KnowledgeEngine(config)
        assert engine._config.max_nodes == 100

    def test_properties(self) -> None:
        engine = KnowledgeEngine()
        assert engine.nodes is not None
        assert engine.edges is not None
        assert engine.temporal is not None
        assert engine.queries is not None
        assert engine.impact_analyzer is not None
        assert engine.architecture_intelligence is not None
        assert engine.healthcare is not None
        assert engine.ai is not None

    def test_create_node(self) -> None:
        engine = KnowledgeEngine()
        node = engine.create_node(NodeType.MODULE, "test-module")
        assert node.name == "test-module"
        assert node.node_type == NodeType.MODULE

    def test_create_node_temporal_event(self) -> None:
        engine = KnowledgeEngine()
        node = engine.create_node(NodeType.MODULE, "m1")
        events = engine.get_entity_history(node.id)
        assert len(events) == 1
        assert events[0].event_type == EventType.NODE_CREATED

    def test_update_node(self) -> None:
        engine = KnowledgeEngine()
        node = engine.create_node(NodeType.MODULE, "old")
        updated = engine.update_node(node.id, name="new")
        assert updated.name == "new"

    def test_update_node_temporal(self) -> None:
        engine = KnowledgeEngine()
        node = engine.create_node(NodeType.MODULE, "m1")
        engine.update_node(node.id, name="m1-updated")
        events = engine.get_entity_history(node.id)
        assert len(events) == 2

    def test_delete_node(self) -> None:
        engine = KnowledgeEngine()
        node = engine.create_node(NodeType.MODULE, "del")
        assert engine.delete_node(node.id) is True
        with pytest.raises(NodeNotFoundError):
            engine.nodes.get_node(node.id)

    def test_create_relationship(self) -> None:
        engine = KnowledgeEngine()
        n1 = engine.create_node(NodeType.MODULE, "a")
        n2 = engine.create_node(NodeType.MODULE, "b")
        edge = engine.create_relationship(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        assert edge.source_id == n1.id
        assert edge.target_id == n2.id

    def test_create_relationship_temporal(self) -> None:
        engine = KnowledgeEngine()
        n1 = engine.create_node(NodeType.MODULE, "a")
        n2 = engine.create_node(NodeType.MODULE, "b")
        edge = engine.create_relationship(n1.id, n2.id, RelationshipType.USES)
        events = engine.get_entity_history(edge.id)
        assert len(events) == 1

    def test_delete_relationship(self) -> None:
        engine = KnowledgeEngine()
        n1 = engine.create_node(NodeType.MODULE, "a")
        n2 = engine.create_node(NodeType.MODULE, "b")
        edge = engine.create_relationship(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        assert engine.delete_relationship(edge.id) is True
        assert engine.edges.count() == 0

    def test_query(self) -> None:
        engine = KnowledgeEngine()
        n1 = engine.create_node(NodeType.MODULE, "a")
        n2 = engine.create_node(NodeType.MODULE, "b")
        engine.create_relationship(n1.id, n2.id, RelationshipType.DEPENDS_ON)
        result = engine.query(QueryType.DEPENDENCY_ANALYSIS, n1.id)
        assert len(result.nodes) >= 1

    def test_analyze_impact(self) -> None:
        engine = KnowledgeEngine()
        target = engine.create_node(NodeType.MODULE, "target")
        for i in range(3):
            svc = engine.create_node(NodeType.SERVICE, f"svc{i}")
            engine.create_relationship(svc.id, target.id, RelationshipType.DEPENDS_ON)
        report = engine.analyze_impact(target.id, ChangeType.MODIFY)
        assert report.total_affected >= 1

    def test_detect_architecture_smells(self) -> None:
        engine = KnowledgeEngine()
        engine.create_node(NodeType.SERVICE, "orphan")
        smells = engine.detect_architecture_smells()
        assert len(smells) >= 1

    def test_architecture_recommendations(self) -> None:
        engine = KnowledgeEngine()
        engine.create_node(NodeType.SERVICE, "orphan")
        recs = engine.get_architecture_recommendations()
        assert len(recs) >= 1

    def test_ai_reason(self) -> None:
        engine = KnowledgeEngine()
        engine.create_node(NodeType.MODULE, "m1")
        result = engine.ai_reason("overview", "architecture")
        assert result.answer != ""

    def test_snapshot_and_restore(self) -> None:
        engine = KnowledgeEngine()
        engine.create_node(NodeType.MODULE, "m1")
        snap = engine.create_snapshot("test")
        engine.create_node(NodeType.MODULE, "m2")
        assert engine.nodes.count() == 2
        engine.restore_snapshot(snap.id)
        assert engine.nodes.count() == 1

    def test_register_healthcare_standard(self) -> None:
        engine = KnowledgeEngine()
        node = engine.register_healthcare_standard("FHIR R4", HealthcareStandard.FHIR)
        assert node.name == "FHIR R4"
        assert node.node_type == NodeType.HEALTHCARE_STANDARD

    def test_create_healthcare_mapping(self) -> None:
        engine = KnowledgeEngine()
        node = engine.register_healthcare_standard("FHIR", HealthcareStandard.FHIR)
        mapping = engine.create_healthcare_mapping(
            node.id, HealthcareStandard.FHIR, HealthcareEntity.CLINICAL_DOCUMENT, "C001"
        )
        assert mapping.code == "C001"

    def test_get_healthcare_summary(self) -> None:
        engine = KnowledgeEngine()
        engine.register_healthcare_standard("HL7", HealthcareStandard.HL7)
        summary = engine.get_healthcare_summary()
        assert summary["total_standards"] == 1

    def test_get_graph_summary(self) -> None:
        engine = KnowledgeEngine()
        engine.create_node(NodeType.MODULE, "m1")
        engine.create_node(NodeType.SERVICE, "s1")
        summary = engine.get_graph_summary()
        assert summary["node_count"] == 2
        assert "nodes_by_type" in summary
        assert "temporal" in summary

    def test_clear(self) -> None:
        engine = KnowledgeEngine()
        engine.create_node(NodeType.MODULE, "m1")
        engine.create_node(NodeType.SERVICE, "s1")
        engine.clear()
        assert engine.nodes.count() == 0
        assert engine.edges.count() == 0

    def test_temporal_disabled(self) -> None:
        config = KnowledgeEngineConfig(enable_temporal=False)
        engine = KnowledgeEngine(config)
        node = engine.create_node(NodeType.MODULE, "m1")
        events = engine.get_entity_history(node.id)
        assert len(events) == 0
