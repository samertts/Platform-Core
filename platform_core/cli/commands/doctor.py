from __future__ import annotations

import argparse
from uuid import uuid4

from platform_core.cli.core.command import Command
from platform_core.doctor.check_registry import CheckRegistry
from platform_core.doctor.engine import DoctorEngine
from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext


class DoctorCommand(Command):
    name = "doctor"

    help = "Analyze project"

    def configure(self, parser: argparse.ArgumentParser) -> None:
        pass

    def execute(self, args: argparse.Namespace) -> int:
        registry = CheckRegistry()
        engine = DoctorEngine(registry)
        context = EngineContext(
            execution_id=uuid4(),
            execution_mode="doctor",
            cancellation_token=CancellationToken(),
        )
        result = engine.run(context)

        report = result.payload
        if report is not None and hasattr(report, "checks"):
            for check in report.checks:
                icon = "\u2714" if check.status.value == "passed" else "\u2718"
                print(f"{icon} {check.name}: {check.message}")

        return 0
