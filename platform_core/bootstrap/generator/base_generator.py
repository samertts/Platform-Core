from abc import ABC
from abc import abstractmethod
from pathlib import Path


class BaseGenerator(ABC):

    def __init__(self, workspace: Path):

        self.workspace = workspace

    @abstractmethod
    def generate(self):

        pass
