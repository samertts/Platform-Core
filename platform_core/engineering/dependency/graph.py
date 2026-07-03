from __future__ import annotations

from collections import defaultdict
from typing import Any


class DependencyGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, Any] = {}
        self.edges: dict[str, set[str]] = defaultdict(set)

    def add_node(self, node: Any) -> None:
        self.nodes[node.id] = node
        self.edges[node.id]

    def add_dependency(
        self,
        capability: str,
        dependency: str,
    ) -> None:
        self.edges[capability].add(dependency)

    def dependencies_of(
        self,
        capability: str,
    ) -> list[str]:
        return sorted(self.edges.get(capability, []))

    def exists(
        self,
        capability: str,
    ) -> bool:
        return capability in self.nodes

    def capabilities(self) -> list[str]:
        return sorted(self.nodes.keys())
