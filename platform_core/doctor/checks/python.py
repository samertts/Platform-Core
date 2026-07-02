import sys

from platform_core.doctor.result import CheckResult


def run(_):

    return CheckResult(

        name="Python",

        passed=sys.version_info >= (3, 10),

        message=sys.version.split()[0],

    )
