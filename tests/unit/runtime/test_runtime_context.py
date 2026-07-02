from platform_core.events import EventBus
from platform_core.kernel.kernel import Kernel
from platform_core.runtime.context import RuntimeContext
from platform_core.services.container import ServiceContainer


def test_runtime_context():

    container = ServiceContainer()

    context = RuntimeContext(
        kernel=Kernel(
            container,
        ),
        container=container,
        events=EventBus(),
    )

    assert context.kernel is not None

    assert context.container is container

    assert context.events is not None
