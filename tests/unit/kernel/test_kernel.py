from platform_core.kernel.kernel import Kernel
from platform_core.kernel.state import KernelState
from platform_core.services.container import ServiceContainer


def test_kernel_lifecycle():

    kernel = Kernel(
        ServiceContainer(),
    )

    assert kernel.lifecycle.state is KernelState.CREATED

    kernel.initialize()

    assert kernel.lifecycle.state is KernelState.INITIALIZED

    kernel.start()

    assert kernel.lifecycle.state is KernelState.RUNNING

    assert kernel.lifecycle.running

    kernel.stop()

    assert kernel.lifecycle.state is KernelState.STOPPED

    assert not kernel.lifecycle.running


def test_kernel_container():

    container = ServiceContainer()

    kernel = Kernel(
        container,
    )

    assert kernel.container is container
