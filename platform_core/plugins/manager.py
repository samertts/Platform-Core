from __future__ import annotations

from platform_core.plugins.plugin import Plugin
from platform_core.plugins.registry import PluginRegistry


class PluginManager:
    def __init__(self) -> None:

        self._registry = PluginRegistry()

    @property
    def registry(
        self,
    ) -> PluginRegistry:

        return self._registry

    def load(
        self,
        plugin: Plugin,
    ) -> None:

        plugin.initialize()

        self._registry.register(plugin)
