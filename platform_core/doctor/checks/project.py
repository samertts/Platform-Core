from __future__ import annotations

from platform_core.doctor.check_result import CheckResult, CheckStatus
from platform_core.doctor.context import DoctorContext


def run(ctx: DoctorContext) -> CheckResult:
    pyproject = ctx.project_root / "pyproject.toml"

    return CheckResult(
        id="project",
        name="Project",
        status=CheckStatus.PASSED if pyproject.exists() else CheckStatus.FAILED,
        message="pyproject.toml",
    )
