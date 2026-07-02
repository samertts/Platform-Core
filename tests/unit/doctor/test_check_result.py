from dataclasses import FrozenInstanceError

import pytest

from platform_core.doctor.check_result import CheckResult, CheckStatus


def test_result_is_immutable():

    result = CheckResult(
        id="python",
        name="Python",
        status=CheckStatus.PASSED,
    )

    with pytest.raises(FrozenInstanceError):
        result.score = 10


def test_result_defaults():

    result = CheckResult(
        id="git",
        name="Git",
        status=CheckStatus.WARNING,
    )

    assert result.score == 0
    assert result.duration == 0.0
    assert result.metadata == {}


def test_status_values():

    assert CheckStatus.PASSED.value == "passed"
    assert CheckStatus.FAILED.value == "failed"
    assert CheckStatus.WARNING.value == "warning"
    assert CheckStatus.SKIPPED.value == "skipped"
