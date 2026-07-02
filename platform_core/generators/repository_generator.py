"""
Repository Generator
"""

from pathlib import Path


class RepositoryGenerator:

    def __init__(self, root: Path):
        self.root = root

    def create(self):

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
