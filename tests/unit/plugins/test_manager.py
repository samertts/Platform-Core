from platform_core.plugins.manager import PluginManager
from platform_core.plugins.plugin import Plugin


class TestPlugin(Plugin):
    def __init__(self):

        self.initialized = False

    def initialize(self) -> None:

        self.initialized = True


def test_manager():

    manager = PluginManager()

    plugin = TestPlugin()

    manager.load(plugin)

    assert plugin.initialized

    assert manager.registry.exists("TestPlugin")
