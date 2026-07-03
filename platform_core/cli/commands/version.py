from __future__ import annotations

import argparse

from platform_core.cli.core.command import Command
from platform_core.version import VERSION


class VersionCommand(Command):
    name = "version"

    help = "Show Platform version"

    def configure(self, parser: argparse.ArgumentParser) -> None:
        pass

    def execute(self, args: argparse.Namespace) -> int:
        print(f"Platform-Core {VERSION.string}")

        return 0
