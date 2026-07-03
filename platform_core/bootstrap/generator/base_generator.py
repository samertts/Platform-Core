from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class BaseGenerator(ABC):
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace

    @abstractmethod
    def generate(self) -> None:
        pass
