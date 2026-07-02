from __future__ import annotations

from platform_core.execution.command import Command
from platform_core.execution.handler import CommandHandler


class CommandDispatcher:
    def dispatch(
        self,
        handler: CommandHandler,
        command: Command,
    ) -> None:

        handler.handle(command)
