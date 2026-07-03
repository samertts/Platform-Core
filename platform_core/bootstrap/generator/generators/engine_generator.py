from __future__ import annotations

from ..base_generator import BaseGenerator
from ..directory_generator import DirectoryGenerator
from ..file_generator import FileGenerator


class EngineGenerator(BaseGenerator):
    def generate(self) -> None:
        engine = self.workspace / "platform_core" / "engines"

        DirectoryGenerator.create(engine)

        FileGenerator.create(
            engine / "__init__.py",
            "",
        )
