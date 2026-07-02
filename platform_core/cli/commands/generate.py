from pathlib import Path

from platform_core.cli.core.command import Command
from platform_core.generator.engine import GeneratorEngine


class GenerateCommand(Command):
    name = "generate"

    help = "Generate platform artifacts"

    def configure(self, parser) -> None:

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

    def execute(self, args) -> int:

        engine = GeneratorEngine()

        if args.kind == "service":
            result = engine.generate_service(
                Path.cwd(),
                args.name,
            )

            print()
            print("Service generated successfully")
            print(f"Directories : {result.created_directories}")
            print(f"Files       : {result.created_files}")
            print()

        return 0
