from platform_core.plugins.plugin import Plugin
from platform_core.plugins.registry import PluginRegistry


class TestPlugin(Plugin):
    def initialize(self) -> None:
        pass


def test_registry():

    registry = PluginRegistry()

    plugin = TestPlugin()

    registry.register(plugin)

    assert registry.exists("TestPlugin")

    assert registry.get("TestPlugin") is plugin
