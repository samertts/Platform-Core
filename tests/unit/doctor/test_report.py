from platform_core.doctor.check_result import CheckResult, CheckStatus
from platform_core.doctor.report import DoctorReport


def test_empty_report():

    report = DoctorReport()

    assert report.total == 0
    assert report.passed == 0
    assert report.failed == 0
    assert report.warnings == 0
    assert report.skipped == 0


def test_report_statistics():

    report = DoctorReport(
        checks=(
            CheckResult(
                id="python",
                name="Python",
                status=CheckStatus.PASSED,
            ),
            CheckResult(
                id="git",
                name="Git",
                status=CheckStatus.FAILED,
            ),
            CheckResult(
                id="ruff",
                name="Ruff",
                status=CheckStatus.WARNING,
            ),
            CheckResult(
                id="mypy",
                name="MyPy",
                status=CheckStatus.SKIPPED,
            ),
        ),
    )

    assert report.total == 4
    assert report.passed == 1
    assert report.failed == 1
    assert report.warnings == 1
    assert report.skipped == 1
