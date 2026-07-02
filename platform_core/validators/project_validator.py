"""
Project Validator
"""

from pathlib import Path


class ProjectValidator:

    REQUIRED = [
        "README.md",
        "pyproject.toml",
        "platform.yaml",
    ]

    def validate(self, root: Path):

        missing = []

        for item in self.REQUIRED:
            if not (root / item).exists():
                missing.append(item)

        return missing
