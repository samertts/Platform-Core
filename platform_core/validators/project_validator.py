"""
Project Validator
"""

from __future__ import annotations

from pathlib import Path


class ProjectValidator:
    REQUIRED = [
        "README.md",
        "pyproject.toml",
        "platform.yaml",
    ]

    def validate(self, root: Path) -> list[str]:
        missing: list[str] = []

        for item in self.REQUIRED:
            if not (root / item).exists():
                missing.append(item)

        return missing
