"""
Platform-Core Engineering Intelligence

Repository dependency graph.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .models import RepositorySnapshot


class RepositoryGraph:
    """
    Represents relationships between repository modules.
    """

    def __init__(self) -> None:

        self._edges: dict[str, set[str]] = defaultdict(set)

        self._nodes: set[str] = set()

    def add_node(self, name: str) -> None:

        self._nodes.add(name)

    def add_edge(
        self,
        source: str,
        target: str,
    ) -> None:

        self._nodes.add(source)

        self._nodes.add(target)

        self._edges[source].add(target)

    def nodes(self) -> list[str]:

        return sorted(self._nodes)

    def neighbours(
        self,
        node: str,
    ) -> list[str]:

        return sorted(self._edges.get(node, set()))

    def edges(self) -> dict[str, list[str]]:

        return {
            node: sorted(targets)
            for node, targets in self._edges.items()
        }

    @classmethod
    def from_snapshot(
        cls,
        snapshot: RepositorySnapshot,
    ) -> "RepositoryGraph":

        graph = cls()

        for module in snapshot.modules:

            graph.add_node(module.name)

        return graph
