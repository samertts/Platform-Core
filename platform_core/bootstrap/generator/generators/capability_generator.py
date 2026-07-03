from __future__ import annotations

from ..base_generator import BaseGenerator
from ..directory_generator import DirectoryGenerator
from ..file_generator import FileGenerator


class CapabilityGenerator(BaseGenerator):
    def generate(self) -> None:
        root = self.workspace / "platform_core" / "capabilities"

        DirectoryGenerator.create(root)

        FileGenerator.create(
            root / "__init__.py",
            "",
        )
