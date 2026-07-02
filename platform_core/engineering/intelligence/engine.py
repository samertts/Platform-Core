"""
Platform-Core Engineering Intelligence Engine
"""

from __future__ import annotations

from pathlib import Path

from .analyzer import EngineeringAnalyzer
from .discovery import DiscoveryEngine
from .graph import RepositoryGraph
from .index import RepositoryIndex
from .scanner import RepositoryScanner


class EngineeringEngine:
    """
    Main orchestration engine.

    Coordinates repository discovery, indexing,
    graph construction and analysis.
    """

    def __init__(self) -> None:

        self.scanner = RepositoryScanner()

        self.discovery = DiscoveryEngine()

        self.index = RepositoryIndex()

        self.analyzer = EngineeringAnalyzer()

    def run(
        self,
        root: Path,
    ):

        snapshot = self.index.build(root)

        graph = RepositoryGraph.from_snapshot(snapshot)

        result = self.analyzer.analyze(self.index)

        return {
            "snapshot": snapshot,
            "graph": graph,
            "analysis": result,
        }
