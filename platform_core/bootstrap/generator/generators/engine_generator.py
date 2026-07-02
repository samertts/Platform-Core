from pathlib import Path

from ..base_generator import BaseGenerator
from ..directory_generator import DirectoryGenerator
from ..file_generator import FileGenerator


class EngineGenerator(BaseGenerator):

    def generate(self):

        engine = self.workspace / "platform_core" / "engines"

        DirectoryGenerator.create(engine)

        FileGenerator.create(
            engine / "__init__.py",
            "",
        )
