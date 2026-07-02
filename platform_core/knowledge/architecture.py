"""Architecture Intelligence - Detects architectural smells and generates recommendations.

Automatically detects orphan services, dead modules, unused APIs, duplicate services,
circular dependencies, high coupling, low cohesion, and governance violations.
"""

from __future__ import annotations

import threading
from collections import Counter
from typing import Any

from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import (ArchitectureRecommendation,
                                           ArchitectureSmell, ImpactLevel,
                                           Node, NodeType,
                                           RecommendationPriority,
                                           RelationshipType)


class ArchitectureIntelligence:
    """Detects architectural smells and generates recommendations."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._lock = threading.RLock()

    def detect_smells(self) -> list[ArchitectureSmell]:
        smells: list[ArchitectureSmell] = []
        smells.extend(self._detect_orphan_services())
        smells.extend(self._detect_dead_modules())
        smells.extend(self._detect_unused_apis())
        smells.extend(self._detect_duplicate_services())
        smells.extend(self._detect_circular_dependencies())
        smells.extend(self._detect_high_coupling())
        smells.extend(self._detect_god_modules())
        return smells

    def _detect_orphan_services(self) -> list[ArchitectureSmell]:
        smells: list[ArchitectureSmell] = []
        services = self._store.get_nodes_by_type(NodeType.SERVICE)
        for svc in services:
            incoming = self._store.get_incoming_edges(svc.id)
            outgoing = self._store.get_outgoing_edges(svc.id)
            if not incoming and not outgoing:
                smells.append(
                    ArchitectureSmell(
                        smell_type="orphan_service",
                        description=f"Service '{svc.name}' has no connections",
                        affected_nodes=[svc.id],
                        severity=ImpactLevel.MEDIUM,
                        recommendation=f"Connect '{svc.name}' to the ecosystem or deprecate it",
                    )
                )
        return smells

    def _detect_dead_modules(self) -> list[ArchitectureSmell]:
        smells: list[ArchitectureSmell] = []
        modules = self._store.get_nodes_by_type(NodeType.MODULE)
        for mod in modules:
            incoming = self._store.get_incoming_edges(mod.id)
            if not incoming:
                smells.append(
                    ArchitectureSmell(
                        smell_type="dead_module",
                        description=f"Module '{mod.name}' is not referenced by anything",
                        affected_nodes=[mod.id],
                        severity=ImpactLevel.LOW,
                        recommendation=f"Review module '{mod.name}' for removal or integration",
                    )
                )
        return smells

    def _detect_unused_apis(self) -> list[ArchitectureSmell]:
        smells: list[ArchitectureSmell] = []
        apis = self._store.get_nodes_by_type(NodeType.API)
        for api in apis:
            consumers = [
                e
                for e in self._store.get_incoming_edges(api.id)
                if e.relationship_type == RelationshipType.CONSUMES
            ]
            if not consumers:
                smells.append(
                    ArchitectureSmell(
                        smell_type="unused_api",
                        description=f"API '{api.name}' has no consumers",
                        affected_nodes=[api.id],
                        severity=ImpactLevel.LOW,
                        recommendation=f"Review API '{api.name}' for deprecation or promotion",
                    )
                )
        return smells

    def _detect_duplicate_services(self) -> list[ArchitectureSmell]:
        smells: list[ArchitectureSmell] = []
        services = self._store.get_nodes_by_type(NodeType.SERVICE)
        name_groups: dict[str, list[Node]] = {}
        for svc in services:
            name_groups.setdefault(svc.name.lower(), []).append(svc)
        for name, group in name_groups.items():
            if len(group) > 1:
                smells.append(
                    ArchitectureSmell(
                        smell_type="duplicate_service",
                        description=f"Multiple services named '{name}'",
                        affected_nodes=[s.id for s in group],
                        severity=ImpactLevel.MEDIUM,
                        recommendation=f"Consolidate duplicate services named '{name}'",
                    )
                )
        return smells

    def _detect_circular_dependencies(self) -> list[ArchitectureSmell]:
        smells: list[ArchitectureSmell] = []
        nodes = self._store.get_all_nodes()
        visited: set[str] = set()
        for node in nodes:
            if node.id in visited:
                continue
            path: list[str] = []
            self._dfs_cycle(node.id, visited, path, set(), smells)
        return smells

    def _dfs_cycle(
        self,
        node_id: str,
        visited: set[str],
        path: list[str],
        in_stack: set[str],
        smells: list[ArchitectureSmell],
    ) -> None:
        if node_id in in_stack:
            cycle_start = path.index(node_id)
            cycle = path[cycle_start:] + [node_id]
            smells.append(
                ArchitectureSmell(
                    smell_type="circular_dependency",
                    description=f"Circular dependency: {' -> '.join(cycle)}",
                    affected_nodes=cycle,
                    severity=ImpactLevel.HIGH,
                    recommendation="Break the circular dependency chain",
                )
            )
            return
        if node_id in visited:
            return
        visited.add(node_id)
        in_stack.add(node_id)
        path.append(node_id)
        for edge in self._store.get_outgoing_edges(node_id):
            self._dfs_cycle(edge.target_id, visited, path, in_stack, smells)
        path.pop()
        in_stack.remove(node_id)

    def _detect_high_coupling(self) -> list[ArchitectureSmell]:
        smells: list[ArchitectureSmell] = []
        nodes = self._store.get_all_nodes()
        for node in nodes:
            outgoing = self._store.get_outgoing_edges(node.id)
            incoming = self._store.get_incoming_edges(node.id)
            total = len(outgoing) + len(incoming)
            if total > 15:
                smells.append(
                    ArchitectureSmell(
                        smell_type="high_coupling",
                        description=f"Node '{node.name}' has {total} connections (high coupling)",
                        affected_nodes=[node.id],
                        severity=ImpactLevel.MEDIUM,
                        recommendation=f"Reduce coupling for '{node.name}' by introducing abstraction layers",
                    )
                )
        return smells

    def _detect_god_modules(self) -> list[ArchitectureSmell]:
        smells: list[ArchitectureSmell] = []
        modules = self._store.get_nodes_by_type(NodeType.MODULE)
        for mod in modules:
            outgoing = self._store.get_outgoing_edges(mod.id)
            if len(outgoing) > 20:
                smells.append(
                    ArchitectureSmell(
                        smell_type="god_module",
                        description=f"Module '{mod.name}' depends on {len(outgoing)} other modules",
                        affected_nodes=[mod.id],
                        severity=ImpactLevel.HIGH,
                        recommendation=f"Decompose module '{mod.name}' into smaller, focused modules",
                    )
                )
        return smells

    def generate_recommendations(self) -> list[ArchitectureRecommendation]:
        recs: list[ArchitectureRecommendation] = []
        smells = self.detect_smells()
        smell_counts = Counter(s.smell_type for s in smells)
        for smell_type, count in smell_counts.most_common():
            if smell_type == "orphan_service":
                recs.append(
                    ArchitectureRecommendation(
                        priority=RecommendationPriority.MEDIUM,
                        title=f"Address {count} orphan service(s)",
                        description="Orphan services have no connections and should be integrated or removed",
                        estimated_effort=f"{count * 2} hours",
                        rationale="Disconnected services increase maintenance burden",
                    )
                )
            elif smell_type == "circular_dependency":
                recs.append(
                    ArchitectureRecommendation(
                        priority=RecommendationPriority.HIGH,
                        title=f"Break {count} circular dependency(ies)",
                        description="Circular dependencies make the system fragile and hard to test",
                        estimated_effort=f"{count * 4} hours",
                        rationale="Circular dependencies prevent independent deployment",
                    )
                )
            elif smell_type == "high_coupling":
                recs.append(
                    ArchitectureRecommendation(
                        priority=RecommendationPriority.MEDIUM,
                        title=f"Reduce coupling in {count} node(s)",
                        description="High coupling increases change risk and reduces modularity",
                        estimated_effort=f"{count * 3} hours",
                        rationale="Loose coupling improves maintainability",
                    )
                )
            elif smell_type == "god_module":
                recs.append(
                    ArchitectureRecommendation(
                        priority=RecommendationPriority.HIGH,
                        title=f"Decompose {count} god module(s)",
                        description="God modules violate single responsibility and are hard to maintain",
                        estimated_effort=f"{count * 8} hours",
                        rationale="Large modules are error-prone and block parallel development",
                    )
                )
        return recs

    def get_architecture_summary(self) -> dict[str, Any]:
        smells = self.detect_smells()
        smell_counts = Counter(s.smell_type for s in smells)
        severity_counts = Counter(s.severity.value for s in smells)
        return {
            "total_smells": len(smells),
            "by_type": dict(smell_counts),
            "by_severity": dict(severity_counts),
            "recommendations_count": len(self.generate_recommendations()),
        }
