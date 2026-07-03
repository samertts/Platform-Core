from platform_core.runtime.runtime import Runtime
from platform_core.services.container import ServiceContainer


def test_runtime_lifecycle() -> None:

    runtime = Runtime(
        ServiceContainer(),
    )

    runtime.initialize()

    runtime.start()

    assert runtime.running

    runtime.stop()

    assert runtime.running is False
