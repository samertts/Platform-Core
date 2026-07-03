from __future__ import annotations

import argparse

from platform_core.cli.core.discovery import discover_commands


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="platform",
        description="Platform-Core",
    )

    sub = parser.add_subparsers()

    for command in discover_commands():
        command.register(sub)

    return parser
