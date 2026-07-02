"""
Platform-Core Engineering Intelligence

Repository Index
"""

from __future__ import annotations

from pathlib import Path

from .ast import PythonAstScanner
from .discovery import DiscoveryEngine
from .graph import RepositoryGraph
from .models import RepositorySnapshot
from .scanner import RepositoryScanner


class RepositoryIndex:
    """
    Central project index.

    Owns all discovered repository information.
    """

    def __init__(self) -> None:

        self._scanner = RepositoryScanner()

        self._discovery = DiscoveryEngine()

        self._ast = PythonAstScanner()

    def build(
        self,
        root: Path,
    ) -> RepositorySnapshot:

        snapshot = self._scanner.scan(root)

        self.discovery = self._discovery.discover(root)

        self.graph = RepositoryGraph.from_snapshot(snapshot)

        self.ast = {}

        for module in snapshot.modules:
            for file in module.files:
                if file.path.suffix == ".py":
                    try:
                        self.ast[file.path] = self._ast.scan(file.path)

                    except Exception:
                        pass

        return snapshot
