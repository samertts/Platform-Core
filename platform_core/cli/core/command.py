from __future__ import annotations

import argparse
from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    name: str = ""

    help: str = ""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """
        Optional hook for subclasses to add command-line arguments.
        """
        pass

    @abstractmethod
    def execute(self, args: argparse.Namespace) -> int:
        """
        Execute the command.
        """
        raise NotImplementedError

    def register(self, subparsers: Any) -> None:
        parser = subparsers.add_parser(
            self.name,
            help=self.help,
        )

        self.configure(parser)

        parser.set_defaults(
            handler=self.execute,
        )
