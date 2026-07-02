from __future__ import annotations

from abc import ABC, abstractmethod

from platform_core.execution.command import Command


class CommandHandler(ABC):
    @abstractmethod
    def handle(
        self,
        command: Command,
    ) -> None:
        raise NotImplementedError
