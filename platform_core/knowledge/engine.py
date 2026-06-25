"""Knowledge Engine - Orchestrator for the Knowledge Graph.

Coordinates all knowledge graph sub-engines and provides the main API.
"""

from __future__ import annotations

import threading
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.nodes import NodeManager
from platform_core.knowledge.edges import EdgeManager
from platform_core.knowledge.temporal import TemporalManager
from platform_core.knowledge.queries import QueryEngine
from platform_core.knowledge.impact import ImpactAnalyzer
from platform_core.knowledge.architecture import ArchitectureIntelligence
from platform_core.knowledge.healthcare import HealthcareKnowledge
from platform_core.knowledge.ai_layer import AIKnowledgeLayer
from platform_core.knowledge.types import (
    AIReasoningResult,
    ArchitectureRecommendation,
    ArchitectureSmell,
    ChangeType,
    Edge,
    EventType,
    GraphSnapshot,
    HealthcareEntity,
    HealthcareMapping,
    HealthcareStandard,
    ImpactReport,
    ImpactLevel,
    KnowledgeEngineConfig,
    LifecycleStage,
    Node,
    NodeStatus,
    NodeType,
    QueryResult,
    QueryType,
    RelationshipStatus,
    RelationshipType,
    TemporalEvent,
)


class KnowledgeEngine:
    """Main orchestrator for the Knowledge Graph Engine.

    Coordinates: GraphStore, NodeManager, EdgeManager, TemporalManager,
    QueryEngine, ImpactAnalyzer, ArchitectureIntelligence, HealthcareKnowledge,
    and AIKnowledgeLayer.
    """

    def __init__(self, config: KnowledgeEngineConfig | None = None) -> None:
        self._config = config or KnowledgeEngineConfig()
        self._store = GraphStore(
            max_nodes=self._config.max_nodes,
            max_edges=self._config.max_edges,
        )
        self._nodes = NodeManager(self._store)
        self._edges = EdgeManager(self._store)
        self._temporal = TemporalManager(self._store)
        self._queries = QueryEngine(self._store)
        self._impact = ImpactAnalyzer(self._store)
        self._architecture = ArchitectureIntelligence(self._store)
        self._healthcare = HealthcareKnowledge(self._store, self._nodes)
        self._ai = AIKnowledgeLayer(self._store)
        self._lock = threading.RLock()

    @property
    def nodes(self) -> NodeManager:
        return self._nodes

    @property
    def edges(self) -> EdgeManager:
        return self._edges

    @property
    def temporal(self) -> TemporalManager:
        return self._temporal

    @property
    def queries(self) -> QueryEngine:
        return self._queries

    @property
    def impact_analyzer(self) -> ImpactAnalyzer:
        return self._impact

    @property
    def architecture_intelligence(self) -> ArchitectureIntelligence:
        return self._architecture

    @property
    def healthcare(self) -> HealthcareKnowledge:
        return self._healthcare

    @property
    def ai(self) -> AIKnowledgeLayer:
        return self._ai

    def create_node(
        self,
        node_type: NodeType,
        name: str,
        **kwargs: Any,
    ) -> Node:
        node = self._nodes.create_node(node_type, name, **kwargs)
        if self._config.enable_temporal:
            self._temporal.record_event(
                EventType.NODE_CREATED,
                node.id,
                NodeType,
                new_value=node.to_dict(),
            )
        return node

    def update_node(self, node_id: str, **kwargs: Any) -> Node:
        old_node = self._nodes.get_node(node_id)
        old_value = old_node.to_dict()
        node = self._nodes.update_node(node_id, **kwargs)
        if self._config.enable_temporal:
            self._temporal.record_event(
                EventType.NODE_UPDATED,
                node_id,
                NodeType,
                old_value=old_value,
                new_value=node.to_dict(),
            )
        return node

    def delete_node(self, node_id: str) -> bool:
        old_node = self._nodes.get_node(node_id)
        old_value = old_node.to_dict() if old_node else None
        result = self._nodes.delete_node(node_id)
        if result and self._config.enable_temporal:
            self._temporal.record_event(
                EventType.NODE_DELETED,
                node_id,
                NodeType,
                old_value=old_value,
            )
        return result

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: RelationshipType,
        **kwargs: Any,
    ) -> Edge:
        edge = self._edges.create_edge(source_id, target_id, relationship_type, **kwargs)
        if self._config.enable_temporal:
            self._temporal.record_event(
                EventType.RELATIONSHIP_CREATED,
                edge.id,
                RelationshipType,
                new_value=edge.to_dict(),
            )
        return edge

    def delete_relationship(self, edge_id: str) -> bool:
        result = self._edges.delete_edge(edge_id)
        if result and self._config.enable_temporal:
            self._temporal.record_event(
                EventType.RELATIONSHIP_DELETED,
                edge_id,
                RelationshipType,
            )
        return result

    def query(self, query_type: QueryType, node_id: str = "", **kwargs: Any) -> QueryResult:
        return self._queries.execute_query(query_type, node_id, **kwargs)

    def analyze_impact(
        self,
        node_id: str,
        change_type: ChangeType = ChangeType.MODIFY,
    ) -> ImpactReport:
        return self._impact.analyze_impact(node_id, change_type)

    def detect_architecture_smells(self) -> list[ArchitectureSmell]:
        return self._architecture.detect_smells()

    def get_architecture_recommendations(self) -> list[ArchitectureRecommendation]:
        return self._architecture.generate_recommendations()

    def ai_reason(
        self,
        question: str,
        reasoning_type: str = "architecture",
        node_id: str = "",
    ) -> AIReasoningResult:
        return self._ai.ask(question, reasoning_type, node_id)

    def create_snapshot(self, description: str = "") -> GraphSnapshot:
        return self._temporal.create_snapshot(description)

    def restore_snapshot(self, snapshot_id: str) -> bool:
        return self._temporal.restore_snapshot(snapshot_id)

    def get_entity_history(self, entity_id: str) -> list[TemporalEvent]:
        return self._temporal.get_entity_history(entity_id)

    def register_healthcare_standard(
        self,
        name: str,
        standard: HealthcareStandard,
        **kwargs: Any,
    ) -> Node:
        return self._healthcare.register_standard(name, standard, **kwargs)

    def create_healthcare_mapping(
        self,
        node_id: str,
        standard: HealthcareStandard,
        entity_type: HealthcareEntity,
        code: str,
        **kwargs: Any,
    ) -> HealthcareMapping:
        return self._healthcare.create_mapping(node_id, standard, entity_type, code, **kwargs)

    def get_healthcare_summary(self) -> dict[str, Any]:
        return self._healthcare.get_healthcare_summary()

    def get_graph_summary(self) -> dict[str, Any]:
        return {
            "node_count": self._store.node_count(),
            "edge_count": self._store.edge_count(),
            "nodes_by_type": {
                nt.value: len(self._store.get_nodes_by_type(nt))
                for nt in NodeType
            },
            "edges_by_type": {
                rt.value: len(self._store.get_edges_by_type(rt))
                for rt in RelationshipType
            },
            "temporal": {
                "event_count": self._temporal.event_count(),
                "snapshot_count": self._temporal.snapshot_count(),
            },
        }

    def clear(self) -> None:
        self._nodes.clear()
        self._edges.clear()
        self._temporal.clear()
        self._healthcare.clear()
