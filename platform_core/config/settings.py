"""
Platform Configuration
"""

from pathlib import Path

import yaml
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    workspace: Path = Path.cwd()

    config_file: Path = Path("platform.yaml")

    log_level: str = "INFO"

    sandbox: bool = True


def load_yaml(path: Path):

    with open(path, "r", encoding="utf-8") as file:

        return yaml.safe_load(file)


settings = Settings()
