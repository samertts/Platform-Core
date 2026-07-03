from __future__ import annotations

import sys
from typing import Any

from platform_core.doctor.check_result import CheckResult, CheckStatus


def run(_: Any) -> CheckResult:
    return CheckResult(
        id="python",
        name="Python",
        status=CheckStatus.PASSED if sys.version_info >= (3, 10) else CheckStatus.FAILED,
        message=sys.version.split()[0],
    )
