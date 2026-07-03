from __future__ import annotations

import argparse
from pathlib import Path

from platform_core.cli.core.command import Command
from platform_core.generator.engine import GeneratorEngine


class GenerateCommand(Command):
    name = "generate"

    help = "Generate platform artifacts"

    def configure(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "kind",
            choices=[
                "service",
            ],
            help="Artifact type to generate.",
        )

        parser.add_argument(
            "name",
            help="Artifact name.",
        )

    def execute(self, args: argparse.Namespace) -> int:
        engine = GeneratorEngine()

        if args.kind == "service":
            result = engine.generate_service(
                Path.cwd(),
                args.name,
            )

            print()
            print("Service generated successfully")
            print(f"Directories : {result.directories_created}")
            print(f"Files       : {result.files_created}")
            print()

        return 0
