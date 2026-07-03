from typing import Any, cast

import pytest

from platform_core.doctor.check import DoctorCheck
from platform_core.doctor.check_result import CheckResult, CheckStatus


class FakeCheck(DoctorCheck):
    id = "fake"

    name = "Fake"

    def run(self) -> CheckResult:

        return CheckResult(
            id=self.id,
            name=self.name,
            status=CheckStatus.PASSED,
        )


def test_fake_check() -> None:

    result = FakeCheck().run()

    assert result.status is CheckStatus.PASSED


def test_base_is_abstract() -> None:

    with pytest.raises(TypeError):
        cast(Any, DoctorCheck)()
