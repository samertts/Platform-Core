from __future__ import annotations

from pathlib import Path

from .generator_registry import GeneratorRegistry


class GeneratorEngine:
    def __init__(self) -> None:
        self.registry = GeneratorRegistry()

    def run(
        self,
        generator_name: str,
        workspace: Path,
    ) -> None:
        generator = self.registry.get(generator_name)

        instance = generator(workspace)

        instance.generate()
