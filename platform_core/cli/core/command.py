from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Command(ABC):

    name: str = ""

    help: str = ""

    def configure(self, parser) -> None:
        """
        Optional hook for subclasses to add command-line arguments.
        """
        pass

    @abstractmethod
    def execute(self, args) -> int:
        """
        Execute the command.
        """
        raise NotImplementedError

    def register(self, subparsers) -> None:

        parser = subparsers.add_parser(
            self.name,
            help=self.help,
        )

        self.configure(parser)

        parser.set_defaults(
            handler=self.execute,
        )
