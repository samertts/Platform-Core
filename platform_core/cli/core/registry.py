from platform_core.cli.commands.bootstrap import BootstrapCommand
from platform_core.cli.commands.doctor import DoctorCommand
from platform_core.cli.commands.generate import GenerateCommand
from platform_core.cli.commands.version import VersionCommand


def load_commands():

    return [

        VersionCommand(),

        DoctorCommand(),

        BootstrapCommand(),

        GenerateCommand(),

    ]
