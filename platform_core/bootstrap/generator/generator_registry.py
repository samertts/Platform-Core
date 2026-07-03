from __future__ import annotations

from .base_generator import BaseGenerator


class GeneratorRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, type[BaseGenerator]] = {}

    def register(
        self,
        name: str,
        generator: type[BaseGenerator],
    ) -> None:
        self._registry[name] = generator

    def get(self, name: str) -> type[BaseGenerator]:
        return self._registry[name]

    def available(self) -> list[str]:
        return sorted(self._registry.keys())
