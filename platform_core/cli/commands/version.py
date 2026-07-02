from platform_core.cli.core.command import Command
from platform_core.version import VERSION


class VersionCommand(Command):

    name = "version"

    help = "Show Platform version"

    def configure(self, parser) -> None:
        pass

    def execute(self, args) -> int:

        print(
            f"Platform-Core {VERSION.string}"
        )

        return 0
