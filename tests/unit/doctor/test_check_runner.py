from platform_core.doctor.check import DoctorCheck
from platform_core.doctor.check_registry import CheckRegistry
from platform_core.doctor.check_result import CheckResult, CheckStatus
from platform_core.doctor.check_runner import CheckRunner


class CheckA(DoctorCheck):
    id = "a"

    name = "A"

    def run(self):

        return CheckResult(
            id=self.id,
            name=self.name,
            status=CheckStatus.PASSED,
            score=10,
        )


class CheckB(DoctorCheck):
    id = "b"

    name = "B"

    def run(self):

        return CheckResult(
            id=self.id,
            name=self.name,
            status=CheckStatus.WARNING,
            score=5,
        )


def test_runner_executes_every_check():

    registry = CheckRegistry()

    registry.register(CheckA())

    registry.register(CheckB())

    report = CheckRunner(registry).run()

    assert report.total == 2

    assert report.score == 15

    assert report.passed == 1

    assert report.warnings == 1


def test_runner_empty_registry():

    registry = CheckRegistry()

    report = CheckRunner(registry).run()

    assert report.total == 0

    assert report.score == 0
