"""Unit tests for Knowledge Graph types."""

from __future__ import annotations

import pytest
from platform_core.knowledge.types import (
    NodeType,
    NodeStatus,
    LifecycleStage,
    RelationshipType,
    RelationshipStatus,
    QueryType,
    ImpactLevel,
    ChangeType,
    SmellType,
    RecommendationPriority,
    HealthcareStandard,
    HealthcareEntity,
    EventType,
    Node,
    Edge,
    GraphSnapshot,
    TemporalEvent,
    QueryResult,
    ImpactReport,
    ArchitectureSmell,
    ArchitectureRecommendation,
    HealthcareMapping,
    AIReasoningResult,
    GraphVisualization,
    KnowledgeEngineConfig,
    KnowledgeError,
    NodeNotFoundError,
    EdgeNotFoundError,
    CircularDependencyError,
    GraphConstraintError,
    TemporalError,
)


class TestEnums:
    def test_node_type(self) -> None:
        assert NodeType.REPOSITORY.value == "repository"
        assert NodeType.MODULE.value == "module"
        assert NodeType.SERVICE.value == "service"
        assert NodeType.API.value == "api"
        assert NodeType.EVENT.value == "event"

    def test_node_status(self) -> None:
        assert NodeStatus.ACTIVE.value == "active"
        assert NodeStatus.INACTIVE.value == "inactive"
        assert NodeStatus.DEPRECATED.value == "deprecated"
        assert NodeStatus.PENDING.value == "pending"
        assert NodeStatus.DRAFT.value == "draft"

    def test_lifecycle_stage(self) -> None:
        assert LifecycleStage.IDEA.value == "idea"
        assert LifecycleStage.PRODUCTION.value == "production"
        assert LifecycleStage.RETIRED.value == "retired"

    def test_relationship_type(self) -> None:
        assert RelationshipType.DEPENDS_ON.value == "depends_on"
        assert RelationshipType.USES.value == "uses"
        assert RelationshipType.IMPLEMENTS.value == "implements"
        assert RelationshipType.GOVERNED_BY.value == "governed_by"

    def test_relationship_status(self) -> None:
        assert RelationshipStatus.ACTIVE.value == "active"
        assert RelationshipStatus.PROPOSED.value == "proposed"
        assert RelationshipStatus.BROKEN.value == "broken"

    def test_query_type(self) -> None:
        assert QueryType.DEPENDENCY_ANALYSIS.value == "dependency_analysis"
        assert QueryType.IMPACT_ANALYSIS.value == "impact_analysis"
        assert QueryType.CIRCULAR_DEPENDENCY.value == "circular_dependency"
        assert QueryType.SHORTEST_PATH.value == "shortest_path"
        assert QueryType.REACHABILITY.value == "reachability"

    def test_impact_level(self) -> None:
        assert ImpactLevel.NONE.value == "none"
        assert ImpactLevel.LOW.value == "low"
        assert ImpactLevel.MEDIUM.value == "medium"
        assert ImpactLevel.HIGH.value == "high"
        assert ImpactLevel.CRITICAL.value == "critical"

    def test_change_type(self) -> None:
        assert ChangeType.ADD.value == "add"
        assert ChangeType.MODIFY.value == "modify"
        assert ChangeType.DELETE.value == "delete"
        assert ChangeType.REPLACE.value == "replace"

    def test_healthcare_standard(self) -> None:
        assert HealthcareStandard.HL7.value == "hl7"
        assert HealthcareStandard.FHIR.value == "fhir"
        assert HealthcareStandard.LOINC.value == "loinc"

    def test_event_type(self) -> None:
        assert EventType.NODE_CREATED.value == "node_created"
        assert EventType.NODE_UPDATED.value == "node_updated"
        assert EventType.SNAPSHOT_CREATED.value == "snapshot_created"

    def test_smell_type(self) -> None:
        assert SmellType.ORPHAN_SERVICE.value == "orphan_service"
        assert SmellType.DEAD_MODULE.value == "dead_module"
        assert SmellType.CIRCULAR_DEPENDENCY.value == "circular_dependency"


class TestDataclasses:
    def test_node_defaults(self) -> None:
        n = Node()
        assert n.id is not None
        assert n.node_type == NodeType.MODULE
        assert n.status == NodeStatus.ACTIVE
        assert n.lifecycle == LifecycleStage.DEVELOPMENT
        assert n.version == "1.0.0"

    def test_node_to_dict(self) -> None:
        n = Node(name="test", node_type=NodeType.SERVICE)
        d = n.to_dict()
        assert d["name"] == "test"
        assert d["node_type"] == "service"
        assert "id" in d
        assert "created_at" in d

    def test_edge_defaults(self) -> None:
        e = Edge()
        assert e.id is not None
        assert e.relationship_type == RelationshipType.DEPENDS_ON
        assert e.status == RelationshipStatus.ACTIVE
        assert e.confidence == 1.0

    def test_edge_to_dict(self) -> None:
        e = Edge(source_id="s", target_id="t", relationship_type=RelationshipType.USES)
        d = e.to_dict()
        assert d["source_id"] == "s"
        assert d["target_id"] == "t"
        assert d["relationship_type"] == "uses"

    def test_graph_snapshot(self) -> None:
        s = GraphSnapshot(description="test snapshot", node_count=5, edge_count=3)
        assert s.description == "test snapshot"
        assert s.node_count == 5
        assert s.edge_count == 3

    def test_temporal_event(self) -> None:
        e = TemporalEvent(event_type=EventType.NODE_CREATED, entity_id="n1")
        assert e.event_type == EventType.NODE_CREATED
        assert e.entity_id == "n1"

    def test_query_result(self) -> None:
        r = QueryResult(query_type=QueryType.DEPENDENCY_ANALYSIS)
        assert r.query_type == QueryType.DEPENDENCY_ANALYSIS
        assert len(r.nodes) == 0
        assert len(r.edges) == 0

    def test_impact_report(self) -> None:
        r = ImpactReport(change_type=ChangeType.MODIFY, impact_level=ImpactLevel.HIGH)
        assert r.change_type == ChangeType.MODIFY
        assert r.impact_level == ImpactLevel.HIGH

    def test_architecture_smell(self) -> None:
        s = ArchitectureSmell(smell_type="orphan_service", severity=ImpactLevel.MEDIUM)
        assert s.smell_type == "orphan_service"
        assert s.severity == ImpactLevel.MEDIUM

    def test_architecture_recommendation(self) -> None:
        r = ArchitectureRecommendation(
            priority=RecommendationPriority.HIGH,
            title="Fix coupling",
        )
        assert r.priority == RecommendationPriority.HIGH
        assert r.title == "Fix coupling"

    def test_healthcare_mapping(self) -> None:
        m = HealthcareMapping(
            node_id="n1",
            standard=HealthcareStandard.FHIR,
            entity_type=HealthcareEntity.CLINICAL_DOCUMENT,
            code="12345",
        )
        assert m.standard == HealthcareStandard.FHIR
        assert m.code == "12345"

    def test_ai_reasoning_result(self) -> None:
        r = AIReasoningResult(reasoning_type="architecture", confidence=0.8)
        assert r.reasoning_type == "architecture"
        assert r.confidence == 0.8

    def test_graph_visualization(self) -> None:
        v = GraphVisualization(title="Test", graph_type="architecture")
        d = v.to_dict()
        assert d["title"] == "Test"
        assert d["graph_type"] == "architecture"

    def test_knowledge_engine_config(self) -> None:
        c = KnowledgeEngineConfig(max_nodes=500, max_edges=1000)
        assert c.max_nodes == 500
        assert c.max_edges == 1000
        assert c.enable_temporal is True


class TestExceptions:
    def test_knowledge_error(self) -> None:
        with pytest.raises(KnowledgeError):
            raise KnowledgeError("test")

    def test_node_not_found_error(self) -> None:
        with pytest.raises(NodeNotFoundError):
            raise NodeNotFoundError("missing")

    def test_edge_not_found_error(self) -> None:
        with pytest.raises(EdgeNotFoundError):
            raise EdgeNotFoundError("missing")

    def test_circular_dependency_error(self) -> None:
        with pytest.raises(CircularDependencyError):
            raise CircularDependencyError("cycle")

    def test_graph_constraint_error(self) -> None:
        with pytest.raises(GraphConstraintError):
            raise GraphConstraintError("limit")

    def test_temporal_error(self) -> None:
        with pytest.raises(TemporalError):
            raise TemporalError("time")
