from platform_core.cli.core.command import Command


class BootstrapCommand(Command):

    name = "bootstrap"

    help = "Bootstrap Platform-Core"

    def configure(self, parser) -> None:
        pass

    def execute(self, args) -> int:

        print(
            "Bootstrap is not implemented yet."
        )

        return 0
