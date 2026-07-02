from uuid import uuid4

from platform_core.doctor.check import DoctorCheck
from platform_core.doctor.check_registry import CheckRegistry
from platform_core.doctor.check_result import CheckResult, CheckStatus
from platform_core.doctor.engine import DoctorEngine
from platform_core.engine.cancellation import CancellationToken
from platform_core.engine.context import EngineContext
from platform_core.engine.result import EngineStatus


class FakeCheck(DoctorCheck):
    id = "python"

    name = "Python"

    def run(self):

        return CheckResult(
            id=self.id,
            name=self.name,
            status=CheckStatus.PASSED,
            score=100,
        )


def test_doctor_engine():

    registry = CheckRegistry()

    registry.register(FakeCheck())

    engine = DoctorEngine(registry)

    result = engine.run(
        EngineContext(
            execution_id=uuid4(),
            execution_mode="normal",
            cancellation_token=CancellationToken(),
        )
    )

    assert result.status is EngineStatus.COMPLETED

    assert result.metrics["checks"] == 1

    assert result.metrics["score"] == 100

    assert result.payload.total == 1
