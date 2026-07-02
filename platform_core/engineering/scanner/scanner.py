from pathlib import Path
from typing import Iterable

import yaml

from platform_core.engineering.registry.models import RegistryEntry
from platform_core.engineering.registry.registry import EngineeringRegistry


class EngineeringScanner:
    """
    Scans the .engineering directory and populates the EngineeringRegistry.
    """

    def __init__(
        self,
        engineering_root: Path,
        registry: EngineeringRegistry,
    ):
        self.root = engineering_root
        self.registry = registry

    def scan(self) -> None:

        for file in self._yaml_files():

            document = self._load(file)

            if document is None:
                continue

            entry = RegistryEntry(
                id=document["id"],
                kind=document.get("kind", "capability"),
                name=document.get("name", document["id"]),
                path=str(file),
                description=document.get("description", ""),
                tags=document.get("tags", []),
                metadata=document,
            )

            self.registry.register(entry)

    def _yaml_files(self) -> Iterable[Path]:

        yield from self.root.rglob("*.yaml")

    def _load(self, file: Path):

        with file.open(
            "r",
            encoding="utf8",
        ) as f:

            return yaml.safe_load(f)
