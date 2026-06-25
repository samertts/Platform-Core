"""AI Knowledge Layer - Provides AI interfaces for reasoning over the knowledge graph.

Supports architecture reasoning, dependency reasoning, impact prediction,
migration planning, refactoring recommendations, governance reasoning,
risk reasoning, and healthcare reasoning.
"""

from __future__ import annotations

import threading
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import (
    AIReasoningResult,
    Node,
    NodeType,
    RelationshipType,
)


class AIKnowledgeLayer:
    """AI-assisted reasoning layer for the knowledge graph."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._lock = threading.RLock()

    def reason_architecture(self, question: str, node_id: str = "") -> AIReasoningResult:
        result = AIReasoningResult(reasoning_type="architecture", question=question)
        if node_id:
            node = self._store.get_node_optional(node_id)
            if node:
                result.supporting_nodes.append(node_id)
                outgoing = self._store.get_outgoing_edges(node_id)
                incoming = self._store.get_incoming_edges(node_id)
                result.answer = (
                    f"Node '{node.name}' ({node.node_type.value}) has "
                    f"{len(outgoing)} outgoing and {len(incoming)} incoming connections. "
                    f"Status: {node.status.value}, Lifecycle: {node.lifecycle.value}"
                )
                result.confidence = 0.8
                if len(outgoing) > 10:
                    result.recommendations.append("Consider reducing dependencies")
                if not incoming and node.node_type == NodeType.SERVICE:
                    result.recommendations.append("Service may be orphaned - verify usage")
        else:
            node_count = self._store.node_count()
            edge_count = self._store.edge_count()
            result.answer = (
                f"Architecture overview: {node_count} nodes, {edge_count} edges. "
                f"Graph density: {edge_count / max(node_count, 1):.2f} edges/node"
            )
            result.confidence = 0.6
        return result

    def reason_dependencies(self, question: str, node_id: str = "") -> AIReasoningResult:
        result = AIReasoningResult(reasoning_type="dependencies", question=question)
        if node_id:
            node = self._store.get_node_optional(node_id)
            if node:
                result.supporting_nodes.append(node_id)
                deps = self._store.get_outgoing_edges(node_id)
                dep_names = []
                for e in deps:
                    target = self._store.get_node_optional(e.target_id)
                    if target:
                        dep_names.append(target.name)
                        result.supporting_nodes.append(target.id)
                result.answer = (
                    f"Node '{node.name}' depends on {len(deps)} nodes: "
                    f"{', '.join(dep_names[:10])}"
                )
                result.confidence = 0.9
                if len(deps) > 15:
                    result.recommendations.append("High dependency count - consider refactoring")
        return result

    def reason_impact(self, question: str, node_id: str = "") -> AIReasoningResult:
        result = AIReasoningResult(reasoning_type="impact", question=question)
        if node_id:
            affected: set[str] = set()
            queue = [node_id]
            visited = set()
            depth = 0
            while queue and depth < 5:
                next_queue = []
                for nid in queue:
                    if nid in visited:
                        continue
                    visited.add(nid)
                    for e in self._store.get_incoming_edges(nid):
                        if e.source_id not in visited:
                            affected.add(e.source_id)
                            next_queue.append(e.source_id)
                            result.supporting_nodes.append(e.source_id)
                queue = next_queue
                depth += 1
            result.answer = (
                f"Changing node {node_id} would potentially impact "
                f"{len(affected)} upstream node(s)"
            )
            result.confidence = 0.7
            if len(affected) > 10:
                result.recommendations.append("High impact change - requires thorough review")
        return result

    def reason_migration(self, question: str, node_id: str = "") -> AIReasoningResult:
        result = AIReasoningResult(reasoning_type="migration", question=question)
        if node_id:
            node = self._store.get_node_optional(node_id)
            if node:
                result.supporting_nodes.append(node_id)
                deps = self._store.get_outgoing_edges(node_id)
                dependents = self._store.get_incoming_edges(node_id)
                result.answer = (
                    f"Migration of '{node.name}': {len(deps)} dependencies to migrate, "
                    f"{len(dependents)} dependents to update"
                )
                result.confidence = 0.7
                if dependents:
                    result.recommendations.append("Coordinate migration with dependent services")
                if deps:
                    result.recommendations.append("Ensure all dependencies support new version")
        return result

    def reason_refactoring(self, question: str, node_id: str = "") -> AIReasoningResult:
        result = AIReasoningResult(reasoning_type="refactoring", question=question)
        if node_id:
            node = self._store.get_node_optional(node_id)
            if node:
                result.supporting_nodes.append(node_id)
                outgoing = self._store.get_outgoing_edges(node_id)
                result.answer = (
                    f"Refactoring analysis for '{node.name}': "
                    f"{len(outgoing)} outgoing connections to consider"
                )
                result.confidence = 0.6
                if len(outgoing) > 10:
                    result.recommendations.append("Consider interface segregation")
                    result.recommendations.append("Evaluate dependency inversion opportunities")
        return result

    def reason_governance(self, question: str, node_id: str = "") -> AIReasoningResult:
        result = AIReasoningResult(reasoning_type="governance", question=question)
        if node_id:
            node = self._store.get_node_optional(node_id)
            if node:
                result.supporting_nodes.append(node_id)
                gov_edges = [
                    e for e in self._store.get_incoming_edges(node_id)
                    if e.relationship_type == RelationshipType.GOVERNED_BY
                ]
                cert_edges = [
                    e for e in self._store.get_incoming_edges(node_id)
                    if e.relationship_type == RelationshipType.CERTIFIED_BY
                ]
                result.answer = (
                    f"Governance status for '{node.name}': "
                    f"{len(gov_edges)} governance rule(s), {len(cert_edges)} certification(s)"
                )
                result.confidence = 0.8
                if not cert_edges:
                    result.recommendations.append("Node lacks certification - initiate review")
                if not gov_edges:
                    result.recommendations.append("Node not governed by any policy")
        return result

    def reason_risk(self, question: str, node_id: str = "") -> AIReasoningResult:
        result = AIReasoningResult(reasoning_type="risk", question=question)
        if node_id:
            node = self._store.get_node_optional(node_id)
            if node:
                result.supporting_nodes.append(node_id)
                outgoing = self._store.get_outgoing_edges(node_id)
                incoming = self._store.get_incoming_edges(node_id)
                risk_score = min(1.0, (len(outgoing) * 0.1 + len(incoming) * 0.05))
                result.answer = (
                    f"Risk assessment for '{node.name}': score {risk_score:.2f}, "
                    f"{len(outgoing)} dependencies, {len(incoming)} dependents"
                )
                result.confidence = 0.7
                if risk_score > 0.7:
                    result.recommendations.append("High risk node - prioritize monitoring")
                if len(incoming) > 5:
                    result.recommendations.append("Many dependents - changes require careful review")
        return result

    def reason_healthcare(self, question: str, node_id: str = "") -> AIReasoningResult:
        result = AIReasoningResult(reasoning_type="healthcare", question=question)
        if node_id:
            node = self._store.get_node_optional(node_id)
            if node:
                result.supporting_nodes.append(node_id)
                result.answer = (
                    f"Healthcare analysis for '{node.name}': "
                    f"Type: {node.node_type.value}, Status: {node.status.value}"
                )
                result.confidence = 0.6
                labels = [l for l in node.labels if l.startswith("hl7") or l.startswith("fhir")]
                if labels:
                    result.recommendations.append(f"Healthcare standards detected: {', '.join(labels)}")
        return result

    def ask(
        self,
        question: str,
        reasoning_type: str = "architecture",
        node_id: str = "",
    ) -> AIReasoningResult:
        dispatch = {
            "architecture": self.reason_architecture,
            "dependencies": self.reason_dependencies,
            "impact": self.reason_impact,
            "migration": self.reason_migration,
            "refactoring": self.reason_refactoring,
            "governance": self.reason_governance,
            "risk": self.reason_risk,
            "healthcare": self.reason_healthcare,
        }
        handler = dispatch.get(reasoning_type, self.reason_architecture)
        return handler(question, node_id)
