from dataclasses import FrozenInstanceError

import pytest

from platform_core.doctor.check_result import CheckResult, CheckStatus


def test_result_is_immutable() -> None:

    result = CheckResult(
        id="python",
        name="Python",
        status=CheckStatus.PASSED,
    )

    with pytest.raises(FrozenInstanceError):
        setattr(result, "score", 10)


def test_result_defaults() -> None:

    result = CheckResult(
        id="git",
        name="Git",
        status=CheckStatus.WARNING,
    )

    assert result.score == 0
    assert result.duration == 0.0
    assert result.metadata == {}


def test_status_values() -> None:

    assert CheckStatus.PASSED.value == "passed"
    assert CheckStatus.FAILED.value == "failed"
    assert CheckStatus.WARNING.value == "warning"
    assert CheckStatus.SKIPPED.value == "skipped"
