"""Visualization Engine - Generates graph visualizations.

Supports architecture graphs, repository graphs, dependency graphs,
service graphs, module graphs, event graphs, healthcare graphs,
device graphs, governance graphs, and knowledge timelines.
"""

from __future__ import annotations

import threading
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import (GraphVisualization, Node, NodeType,
                                           RelationshipType)


class VisualizationEngine:
    """Generates graph visualizations for different graph types."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._lock = threading.RLock()

    def generate_architecture_graph(self) -> GraphVisualization:
        nodes = self._store.get_all_nodes()
        edges = self._store.get_all_edges()
        vis_nodes = [
            {
                "id": n.id,
                "label": n.name,
                "type": n.node_type.value,
                "status": n.status.value,
                "lifecycle": n.lifecycle.value,
            }
            for n in nodes
        ]
        vis_edges = [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.relationship_type.value,
            }
            for e in edges
        ]
        return GraphVisualization(
            title="Architecture Graph",
            graph_type="architecture",
            nodes=vis_nodes,
            edges=vis_edges,
            layout="force_directed",
        )

    def generate_repository_graph(self) -> GraphVisualization:
        nodes = self._store.get_nodes_by_type(NodeType.REPOSITORY)
        edges = self._store.get_all_edges()
        node_ids = {n.id for n in nodes}
        vis_edges = [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.relationship_type.value,
            }
            for e in edges
            if e.source_id in node_ids or e.target_id in node_ids
        ]
        vis_nodes = [
            {
                "id": n.id,
                "label": n.name,
                "type": "repository",
                "status": n.status.value,
            }
            for n in nodes
        ]
        return GraphVisualization(
            title="Repository Graph",
            graph_type="repository",
            nodes=vis_nodes,
            edges=vis_edges,
            layout="hierarchical",
        )

    def generate_dependency_graph(self, node_id: str = "") -> GraphVisualization:
        if node_id:
            result_nodes: list[Node] = []
            queue = [node_id]
            visited: set[str] = set()
            for _ in range(10):
                next_queue = []
                for nid in queue:
                    if nid in visited:
                        continue
                    visited.add(nid)
                    node = self._store.get_node_optional(nid)
                    if node:
                        result_nodes.append(node)
                    for e in self._store.get_outgoing_edges(nid):
                        if e.target_id not in visited:
                            next_queue.append(e.target_id)
                queue = next_queue
                if not queue:
                    break
            node_ids = {n.id for n in result_nodes}
            edges = [
                e
                for e in self._store.get_all_edges()
                if e.source_id in node_ids and e.target_id in node_ids
            ]
        else:
            result_nodes = self._store.get_all_nodes()
            edges = self._store.get_all_edges()
            node_ids = {n.id for n in result_nodes}

        vis_nodes = [
            {"id": n.id, "label": n.name, "type": n.node_type.value}
            for n in result_nodes
        ]
        vis_edges = [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.relationship_type.value,
            }
            for e in edges
        ]
        return GraphVisualization(
            title="Dependency Graph",
            graph_type="dependency",
            nodes=vis_nodes,
            edges=vis_edges,
            layout="tree",
        )

    def generate_service_graph(self) -> GraphVisualization:
        nodes = self._store.get_nodes_by_type(NodeType.SERVICE)
        edges = self._store.get_all_edges()
        node_ids = {n.id for n in nodes}
        vis_edges = [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.relationship_type.value,
            }
            for e in edges
            if e.source_id in node_ids or e.target_id in node_ids
        ]
        vis_nodes = [
            {"id": n.id, "label": n.name, "type": "service", "status": n.status.value}
            for n in nodes
        ]
        return GraphVisualization(
            title="Service Graph",
            graph_type="service",
            nodes=vis_nodes,
            edges=vis_edges,
            layout="force_directed",
        )

    def generate_module_graph(self) -> GraphVisualization:
        nodes = self._store.get_nodes_by_type(NodeType.MODULE)
        edges = self._store.get_all_edges()
        node_ids = {n.id for n in nodes}
        vis_edges = [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.relationship_type.value,
            }
            for e in edges
            if e.source_id in node_ids and e.target_id in node_ids
        ]
        vis_nodes = [
            {
                "id": n.id,
                "label": n.name,
                "type": "module",
                "lifecycle": n.lifecycle.value,
            }
            for n in nodes
        ]
        return GraphVisualization(
            title="Module Graph",
            graph_type="module",
            nodes=vis_nodes,
            edges=vis_edges,
            layout="force_directed",
        )

    def generate_event_graph(self) -> GraphVisualization:
        nodes = self._store.get_nodes_by_type(NodeType.EVENT)
        edges = self._store.get_all_edges()
        node_ids = {n.id for n in nodes}
        vis_edges = [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.relationship_type.value,
            }
            for e in edges
            if e.source_id in node_ids or e.target_id in node_ids
        ]
        vis_nodes = [{"id": n.id, "label": n.name, "type": "event"} for n in nodes]
        return GraphVisualization(
            title="Event Graph",
            graph_type="event",
            nodes=vis_nodes,
            edges=vis_edges,
            layout="flow",
        )

    def generate_healthcare_graph(self) -> GraphVisualization:
        nodes = self._store.get_nodes_by_type(NodeType.HEALTHCARE_STANDARD)
        device_nodes = self._store.get_nodes_by_type(NodeType.DEVICE)
        all_nodes = nodes + device_nodes
        edges = self._store.get_all_edges()
        node_ids = {n.id for n in all_nodes}
        vis_edges = [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.relationship_type.value,
            }
            for e in edges
            if e.source_id in node_ids or e.target_id in node_ids
        ]
        vis_nodes = [
            {"id": n.id, "label": n.name, "type": n.node_type.value, "labels": n.labels}
            for n in all_nodes
        ]
        return GraphVisualization(
            title="Healthcare Graph",
            graph_type="healthcare",
            nodes=vis_nodes,
            edges=vis_edges,
            layout="domain",
        )

    def generate_device_graph(self) -> GraphVisualization:
        nodes = self._store.get_nodes_by_type(NodeType.DEVICE)
        edges = self._store.get_all_edges()
        node_ids = {n.id for n in nodes}
        vis_edges = [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.relationship_type.value,
            }
            for e in edges
            if e.source_id in node_ids or e.target_id in node_ids
        ]
        vis_nodes = [
            {"id": n.id, "label": n.name, "type": "device", "status": n.status.value}
            for n in nodes
        ]
        return GraphVisualization(
            title="Device Graph",
            graph_type="device",
            nodes=vis_nodes,
            edges=vis_edges,
            layout="physical",
        )

    def generate_governance_graph(self) -> GraphVisualization:
        policies = self._store.get_nodes_by_type(NodeType.POLICY)
        certs = self._store.get_nodes_by_type(NodeType.CERTIFICATION)
        all_nodes = policies + certs
        edges = self._store.get_all_edges()
        gov_edges = [
            e
            for e in edges
            if e.relationship_type
            in (
                RelationshipType.GOVERNED_BY,
                RelationshipType.CERTIFIED_BY,
            )
        ]
        node_ids = {n.id for n in all_nodes}
        for e in gov_edges:
            node_ids.add(e.source_id)
            node_ids.add(e.target_id)
        all_relevant_nodes = [
            n for n in self._store.get_all_nodes() if n.id in node_ids
        ]
        vis_nodes = [
            {"id": n.id, "label": n.name, "type": n.node_type.value}
            for n in all_relevant_nodes
        ]
        vis_edges = [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "type": e.relationship_type.value,
            }
            for e in gov_edges
        ]
        return GraphVisualization(
            title="Governance Graph",
            graph_type="governance",
            nodes=vis_nodes,
            edges=vis_edges,
            layout="hierarchical",
        )

    def generate_knowledge_timeline(self) -> GraphVisualization:
        nodes = self._store.get_all_nodes()
        vis_nodes = [
            {
                "id": n.id,
                "label": n.name,
                "type": n.node_type.value,
                "created": n.created_at.isoformat(),
                "updated": n.updated_at.isoformat(),
                "lifecycle": n.lifecycle.value,
            }
            for n in sorted(nodes, key=lambda x: x.created_at)
        ]
        return GraphVisualization(
            title="Knowledge Timeline",
            graph_type="timeline",
            nodes=vis_nodes,
            edges=[],
            layout="timeline",
        )

    def generate_visualization(
        self, graph_type: str, node_id: str = ""
    ) -> GraphVisualization:
        dispatch = {
            "architecture": lambda: self.generate_architecture_graph(),
            "repository": lambda: self.generate_repository_graph(),
            "dependency": lambda: self.generate_dependency_graph(node_id),
            "service": lambda: self.generate_service_graph(),
            "module": lambda: self.generate_module_graph(),
            "event": lambda: self.generate_event_graph(),
            "healthcare": lambda: self.generate_healthcare_graph(),
            "device": lambda: self.generate_device_graph(),
            "governance": lambda: self.generate_governance_graph(),
            "timeline": lambda: self.generate_knowledge_timeline(),
        }
        handler = dispatch.get(graph_type)
        if handler:
            return handler()
        return GraphVisualization(
            title=f"Unknown graph type: {graph_type}",
            graph_type="unknown",
        )
