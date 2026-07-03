"""
Platform Configuration
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _build_settings_class() -> type[Any]:
    try:
        from pydantic_settings import BaseSettings  # type: ignore[import-not-found]

        class _Settings(BaseSettings):  # type: ignore[misc]
            workspace: Path = Path.cwd()
            config_file: Path = Path("platform.yaml")
            log_level: str = "INFO"
            sandbox: bool = True

        return _Settings
    except ImportError:
        from pydantic import BaseModel

        class _FallbackSettings(BaseModel):
            workspace: Path = Path.cwd()
            config_file: Path = Path("platform.yaml")
            log_level: str = "INFO"
            sandbox: bool = True

        return _FallbackSettings


Settings = _build_settings_class()


def load_yaml(path: Path) -> Any:
    with open(path, encoding="utf-8") as file:
        return yaml.safe_load(file)


settings = Settings()
