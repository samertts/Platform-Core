"""Knowledge Graph API - REST endpoints for knowledge graph operations.

Exposes: Knowledge API, Relationship API, Dependency API, Impact API,
Search API, Traversal API, History API, Analytics API.
"""

from __future__ import annotations

from typing import Any

from platform_core.knowledge.engine import KnowledgeEngine
from platform_core.knowledge.types import (ChangeType, EdgeNotFoundError,
                                           HealthcareEntity,
                                           HealthcareStandard, ImpactLevel,
                                           KnowledgeError, LifecycleStage,
                                           NodeNotFoundError, NodeStatus,
                                           NodeType, QueryType,
                                           RelationshipType)


class KnowledgeAPI:
    """REST API layer for the Knowledge Graph Engine."""

    def __init__(self, engine: KnowledgeEngine) -> None:
        self._engine = engine

    def create_node(
        self,
        node_type: str,
        name: str,
        version: str = "1.0.0",
        owner: str = "",
        metadata: dict[str, Any] | None = None,
        labels: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        nt = NodeType(node_type)
        node = self._engine.create_node(
            nt,
            name,
            version=version,
            owner=owner,
            metadata=metadata,
            labels=labels,
            tags=tags,
        )
        return {"status": "created", "node": node.to_dict()}

    def get_node(self, node_id: str) -> dict[str, Any]:
        node = self._engine.nodes.get_node(node_id)
        return {"node": node.to_dict()}

    def update_node(self, node_id: str, **kwargs: Any) -> dict[str, Any]:
        node = self._engine.update_node(node_id, **kwargs)
        return {"status": "updated", "node": node.to_dict()}

    def delete_node(self, node_id: str) -> dict[str, Any]:
        result = self._engine.delete_node(node_id)
        return {"status": "deleted" if result else "not_found"}

    def list_nodes(
        self,
        node_type: str | None = None,
        status: str | None = None,
        owner: str | None = None,
    ) -> dict[str, Any]:
        nt = NodeType(node_type) if node_type else None
        st = NodeStatus(status) if status else None
        nodes = self._engine.nodes.list_nodes(node_type=nt, status=st, owner=owner)
        return {"nodes": [n.to_dict() for n in nodes], "count": len(nodes)}

    def search_nodes(self, query: str) -> dict[str, Any]:
        nodes = self._engine.nodes.search_nodes(query)
        return {"nodes": [n.to_dict() for n in nodes], "count": len(nodes)}

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        rt = RelationshipType(relationship_type)
        edge = self._engine.create_relationship(
            source_id,
            target_id,
            rt,
            confidence=confidence,
            metadata=metadata,
        )
        return {"status": "created", "edge": edge.to_dict()}

    def get_relationship(self, edge_id: str) -> dict[str, Any]:
        edge = self._engine.edges.get_edge(edge_id)
        return {"edge": edge.to_dict()}

    def delete_relationship(self, edge_id: str) -> dict[str, Any]:
        result = self._engine.delete_relationship(edge_id)
        return {"status": "deleted" if result else "not_found"}

    def list_relationships(
        self,
        source_id: str | None = None,
        target_id: str | None = None,
        relationship_type: str | None = None,
    ) -> dict[str, Any]:
        rt = RelationshipType(relationship_type) if relationship_type else None
        edges = self._engine.edges.list_edges(
            source_id=source_id,
            target_id=target_id,
            relationship_type=rt,
        )
        return {"edges": [e.to_dict() for e in edges], "count": len(edges)}

    def dependency_analysis(self, node_id: str, max_depth: int = 10) -> dict[str, Any]:
        result = self._engine.query(
            QueryType.DEPENDENCY_ANALYSIS,
            node_id,
            max_depth=max_depth,
        )
        return {
            "nodes": [n.to_dict() for n in result.nodes],
            "edges": [e.to_dict() for e in result.edges],
            "execution_time_ms": result.execution_time_ms,
        }

    def impact_analysis(
        self, node_id: str, change_type: str = "modify"
    ) -> dict[str, Any]:
        ct = ChangeType(change_type)
        report = self._engine.analyze_impact(node_id, ct)
        return {
            "impact_level": report.impact_level.value,
            "total_affected": report.total_affected,
            "affected_repositories": report.affected_repositories,
            "affected_services": report.affected_services,
            "affected_apis": report.affected_apis,
            "affected_events": report.affected_events,
            "affected_devices": report.affected_devices,
            "affected_workflows": report.affected_workflows,
            "affected_packages": report.affected_packages,
            "affected_standards": report.affected_standards,
            "affected_deployments": report.affected_deployments,
            "recommendations": report.recommendations,
        }

    def shortest_path(self, source_id: str, target_id: str) -> dict[str, Any]:
        result = self._engine.query(
            QueryType.SHORTEST_PATH,
            source_id,
            target_id=target_id,
        )
        return {
            "paths": result.paths,
            "found": result.metadata.get("found", False),
            "length": result.metadata.get("length", -1),
        }

    def circular_dependencies(self) -> dict[str, Any]:
        result = self._engine.query(QueryType.CIRCULAR_DEPENDENCY)
        return {
            "cycles": result.paths,
            "cycle_count": result.metadata.get("cycle_count", 0),
        }

    def architecture_navigation(self, node_id: str, depth: int = 3) -> dict[str, Any]:
        result = self._engine.query(
            QueryType.ARCHITECTURE_NAVIGATION,
            node_id,
            depth=depth,
        )
        return {
            "nodes": [n.to_dict() for n in result.nodes],
            "edges": [e.to_dict() for e in result.edges],
        }

    def architecture_smells(self) -> dict[str, Any]:
        smells = self._engine.detect_architecture_smells()
        return {
            "smells": [
                {
                    "type": s.smell_type,
                    "description": s.description,
                    "severity": s.severity.value,
                    "recommendation": s.recommendation,
                }
                for s in smells
            ],
            "count": len(smells),
        }

    def architecture_recommendations(self) -> dict[str, Any]:
        recs = self._engine.get_architecture_recommendations()
        return {
            "recommendations": [
                {
                    "priority": r.priority.value,
                    "title": r.title,
                    "description": r.description,
                    "estimated_effort": r.estimated_effort,
                }
                for r in recs
            ],
            "count": len(recs),
        }

    def ai_reason(
        self,
        question: str,
        reasoning_type: str = "architecture",
        node_id: str = "",
    ) -> dict[str, Any]:
        result = self._engine.ai_reason(question, reasoning_type, node_id)
        return {
            "answer": result.answer,
            "confidence": result.confidence,
            "recommendations": result.recommendations,
            "reasoning_type": result.reasoning_type,
        }

    def create_snapshot(self, description: str = "") -> dict[str, Any]:
        snapshot = self._engine.create_snapshot(description)
        return {
            "snapshot_id": snapshot.id,
            "node_count": snapshot.node_count,
            "edge_count": snapshot.edge_count,
        }

    def get_entity_history(self, entity_id: str) -> dict[str, Any]:
        events = self._engine.get_entity_history(entity_id)
        return {
            "events": [
                {
                    "event_type": e.event_type.value,
                    "timestamp": e.timestamp.isoformat(),
                    "entity_id": e.entity_id,
                }
                for e in events
            ],
            "count": len(events),
        }

    def healthcare_summary(self) -> dict[str, Any]:
        return self._engine.get_healthcare_summary()

    def graph_summary(self) -> dict[str, Any]:
        return self._engine.get_graph_summary()

    def health_check(self) -> dict[str, Any]:
        return {
            "status": "healthy",
            "node_count": self._engine._store.node_count(),
            "edge_count": self._engine._store.edge_count(),
        }
