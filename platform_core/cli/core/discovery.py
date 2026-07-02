from __future__ import annotations

import importlib
import inspect
import pkgutil

from platform_core.cli.core.command import Command
import platform_core.cli.commands as commands_pkg


def discover_commands():

    commands = []

    for module in pkgutil.iter_modules(commands_pkg.__path__):

        mod = importlib.import_module(
            f"{commands_pkg.__name__}.{module.name}"
        )

        for _, obj in inspect.getmembers(mod, inspect.isclass):

            if (
                issubclass(obj, Command)
                and obj is not Command
            ):
                commands.append(obj())

    commands.sort(key=lambda c: c.name)

    return commands
