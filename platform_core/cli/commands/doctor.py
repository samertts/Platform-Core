from platform_core.cli.core.command import Command
from platform_core.doctor.engine import DoctorEngine


class DoctorCommand(Command):
    name = "doctor"

    help = "Analyze project"

    def configure(self, parser) -> None:
        pass

    def execute(self, args) -> int:

        engine = DoctorEngine()

        results = engine.run()

        for result in results:
            icon = "✔" if result.passed else "✘"

            print(f"{icon} {result.name}: {result.message}")

        return 0
