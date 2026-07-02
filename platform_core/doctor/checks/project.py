from platform_core.doctor.result import CheckResult


def run(ctx):

    pyproject = ctx.root / "pyproject.toml"

    return CheckResult(

        name="Project",

        passed=pyproject.exists(),

        message="pyproject.toml",

    )
