from platform_core.plugins.plugin import Plugin


class TestPlugin(Plugin):
    def initialize(self) -> None:
        pass


def test_plugin():

    plugin = TestPlugin()

    assert plugin.name == "TestPlugin"
