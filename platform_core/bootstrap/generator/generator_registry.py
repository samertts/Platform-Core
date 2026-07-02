from .base_generator import BaseGenerator


class GeneratorRegistry:
    def __init__(self):

        self._registry: dict[str, type[BaseGenerator]] = {}

    def register(
        self,
        name: str,
        generator: type[BaseGenerator],
    ):

        self._registry[name] = generator

    def get(self, name: str):

        return self._registry[name]

    def available(self):

        return sorted(self._registry.keys())
