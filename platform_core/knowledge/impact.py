"""Impact Analyzer - Analyzes the impact of changes across the ecosystem.

Determines affected repositories, services, APIs, events, devices,
workflows, packages, standards, and deployments.
"""

from __future__ import annotations

import threading
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import (ChangeType, ImpactLevel,
                                           ImpactReport, Node, NodeType)


class ImpactAnalyzer:
    """Analyzes the impact of changes across the knowledge graph."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._lock = threading.RLock()

    def analyze_impact(
        self,
        source_node_id: str,
        change_type: ChangeType = ChangeType.MODIFY,
        max_depth: int = 10,
    ) -> ImpactReport:
        affected_nodes = self._traverse_upstream(source_node_id, max_depth)
        report = ImpactReport(
            change_type=change_type,
            source_node_id=source_node_id,
        )
        for node in affected_nodes:
            self._categorize_node(node, report)
        report.total_affected = (
            len(report.affected_repositories)
            + len(report.affected_services)
            + len(report.affected_apis)
            + len(report.affected_events)
            + len(report.affected_devices)
            + len(report.affected_workflows)
            + len(report.affected_packages)
            + len(report.affected_standards)
            + len(report.affected_deployments)
        )
        report.impact_level = self._calculate_impact_level(report)
        report.recommendations = self._generate_recommendations(report)
        return report

    def _traverse_upstream(self, node_id: str, max_depth: int) -> list[Node]:
        visited: set[str] = set()
        result: list[Node] = []
        queue: list[tuple[str, int]] = [(node_id, 0)]
        while queue:
            current_id, depth = queue.pop(0)
            if current_id in visited or depth > max_depth:
                continue
            visited.add(current_id)
            for edge in self._store.get_incoming_edges(current_id):
                if edge.source_id not in visited:
                    node = self._store.get_node_optional(edge.source_id)
                    if node:
                        result.append(node)
                    queue.append((edge.source_id, depth + 1))
        return result

    def _categorize_node(self, node: Node, report: ImpactReport) -> None:
        name = node.name or node.id
        if node.node_type == NodeType.REPOSITORY:
            if name not in report.affected_repositories:
                report.affected_repositories.append(name)
        elif node.node_type == NodeType.SERVICE:
            if name not in report.affected_services:
                report.affected_services.append(name)
        elif node.node_type == NodeType.API:
            if name not in report.affected_apis:
                report.affected_apis.append(name)
        elif node.node_type == NodeType.EVENT:
            if name not in report.affected_events:
                report.affected_events.append(name)
        elif node.node_type == NodeType.DEVICE:
            if name not in report.affected_devices:
                report.affected_devices.append(name)
        elif node.node_type == NodeType.WORKFLOW:
            if name not in report.affected_workflows:
                report.affected_workflows.append(name)
        elif node.node_type == NodeType.PACKAGE:
            if name not in report.affected_packages:
                report.affected_packages.append(name)
        elif node.node_type == NodeType.HEALTHCARE_STANDARD:
            if name not in report.affected_standards:
                report.affected_standards.append(name)
        elif node.node_type == NodeType.DEPLOYMENT:
            if name not in report.affected_deployments:
                report.affected_deployments.append(name)

    def _calculate_impact_level(self, report: ImpactReport) -> ImpactLevel:
        total = report.total_affected
        if total == 0:
            return ImpactLevel.NONE
        if total <= 3:
            return ImpactLevel.LOW
        if total <= 10:
            return ImpactLevel.MEDIUM
        if total <= 25:
            return ImpactLevel.HIGH
        return ImpactLevel.CRITICAL

    def _generate_recommendations(self, report: ImpactReport) -> list[str]:
        recs: list[str] = []
        if report.impact_level == ImpactLevel.CRITICAL:
            recs.append("CRITICAL: Comprehensive review required before proceeding")
        if report.affected_services:
            recs.append(
                f"Review {len(report.affected_services)} affected service(s) for compatibility"
            )
        if report.affected_apis:
            recs.append(
                f"Validate {len(report.affected_apis)} affected API(s) for breaking changes"
            )
        if report.affected_deployments:
            recs.append(
                f"Plan deployment updates for {len(report.affected_deployments)} deployment(s)"
            )
        if report.affected_packages:
            recs.append(f"Rebuild {len(report.affected_packages)} affected package(s)")
        if not recs:
            recs.append("No specific recommendations - low impact change")
        return recs
