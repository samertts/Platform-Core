from __future__ import annotations

import argparse

from platform_core.cli.core.command import Command


class BootstrapCommand(Command):
    name = "bootstrap"

    help = "Bootstrap Platform-Core"

    def configure(self, parser: argparse.ArgumentParser) -> None:
        pass

    def execute(self, args: argparse.Namespace) -> int:
        print("Bootstrap is not implemented yet.")

        return 0
