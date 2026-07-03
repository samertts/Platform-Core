from __future__ import annotations

from pathlib import Path


class DirectoryGenerator:
    @staticmethod
    def create(path: Path) -> None:
        path.mkdir(
            parents=True,
            exist_ok=True,
        )
