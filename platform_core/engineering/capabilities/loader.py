from pathlib import Path

import yaml

from .models import Capability


class CapabilityLoader:
    def __init__(self, root: Path):

        self.root = root

    def load(self):

        capabilities = []

        for file in self.root.rglob("*.yaml"):
            with open(file, encoding="utf-8") as f:
                data = yaml.safe_load(f)

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
