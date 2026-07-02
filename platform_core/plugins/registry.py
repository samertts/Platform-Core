from __future__ import annotations

from platform_core.plugins.plugin import Plugin


class PluginRegistry:
    def __init__(self) -> None:

        self._plugins: dict[str, Plugin] = {}

    def register(
        self,
        plugin: Plugin,
    ) -> None:

        self._plugins[plugin.name] = plugin

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._plugins

    def get(
        self,
        name: str,
    ) -> Plugin:

        return self._plugins[name]

    @property
    def plugins(
        self,
    ) -> tuple[Plugin, ...]:

        return tuple(self._plugins.values())
