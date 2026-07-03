from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import Capability


class CapabilityLoader:
    def __init__(self, root: Path) -> None:
        self.root = root

    def load(self) -> list[Capability]:
        capabilities: list[Capability] = []

        for file in self.root.rglob("*.yaml"):
            with open(file, encoding="utf-8") as f:
                data: dict[str, Any] = yaml.safe_load(f)

            capabilities.append(
                Capability(
                    id=data["id"],
                    name=data["name"],
                    owner=data["owner"],
                    status=data["status"],
                    description=data["description"],
                    provides=data.get("provides", []),
                    depends_on=data.get("depends_on", []),
                    required_by=data.get("required_by", []),
                    tags=data.get("tags", []),
                )
            )

        return capabilities
