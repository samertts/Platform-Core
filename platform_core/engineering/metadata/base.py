from pathlib import Path
from typing import Any

import yaml


class BaseMetadataLoader:
    def load_yaml(self, path: Path) -> Any:
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def exists(self, path: Path) -> bool:

        return path.exists()
