from platform_core.kernel.kernel import Kernel
from platform_core.kernel.state import KernelState
from platform_core.services.container import ServiceContainer


def test_kernel_lifecycle() -> None:

    kernel = Kernel(
        ServiceContainer(),
    )

    state: KernelState = kernel.lifecycle.state
    assert state == KernelState.CREATED

    kernel.initialize()
    state = kernel.lifecycle.state
    assert state == KernelState.INITIALIZED

    kernel.start()
    state = kernel.lifecycle.state
    assert state == KernelState.RUNNING

    assert kernel.lifecycle.running

    kernel.stop()
    state = kernel.lifecycle.state
    assert state == KernelState.STOPPED

    assert not kernel.lifecycle.running


def test_kernel_container() -> None:

    container = ServiceContainer()

    kernel = Kernel(
        container,
    )

    assert kernel.container is container
