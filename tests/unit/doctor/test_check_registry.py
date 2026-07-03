import pytest

from platform_core.doctor.check import DoctorCheck
from platform_core.doctor.check_registry import CheckRegistry
from platform_core.doctor.check_result import CheckResult, CheckStatus


class FakeCheck(DoctorCheck):
    id = "python"

    name = "Python"

    def run(self) -> CheckResult:

        return CheckResult(
            id=self.id,
            name=self.name,
            status=CheckStatus.PASSED,
        )


def test_register() -> None:

    registry = CheckRegistry()

    registry.register(FakeCheck())

    assert len(registry) == 1


def test_get() -> None:

    registry = CheckRegistry()

    registry.register(FakeCheck())

    assert registry.get("python").id == "python"


def test_exists() -> None:

    registry = CheckRegistry()

    registry.register(FakeCheck())

    assert registry.exists("python")


def test_duplicate() -> None:

    registry = CheckRegistry()

    registry.register(FakeCheck())

    with pytest.raises(ValueError):
        registry.register(FakeCheck())


def test_unregister() -> None:

    registry = CheckRegistry()

    registry.register(FakeCheck())

    registry.unregister("python")

    assert len(registry) == 0


def test_clear() -> None:

    registry = CheckRegistry()

    registry.register(FakeCheck())

    registry.clear()

    assert len(registry) == 0
