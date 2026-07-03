from __future__ import annotations

from platform_core.cli.commands.bootstrap import BootstrapCommand
from platform_core.cli.commands.doctor import DoctorCommand
from platform_core.cli.commands.generate import GenerateCommand
from platform_core.cli.commands.version import VersionCommand
from platform_core.cli.core.command import Command


def load_commands() -> list[Command]:
    return [
        VersionCommand(),
        DoctorCommand(),
        BootstrapCommand(),
        GenerateCommand(),
    ]
