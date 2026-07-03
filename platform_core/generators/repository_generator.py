"""
Repository Generator
"""

from __future__ import annotations

from pathlib import Path


class RepositoryGenerator:
    def __init__(self, root: Path) -> None:
        self.root = root

    def create(self) -> None:
        directories = [
            "docs",
            "tests",
            "examples",
            "templates",
            "schemas",
            "manifests",
        ]

        for directory in directories:
            path = self.root / directory
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created {path}")
