from .state import KernelState


class Lifecycle:
    def __init__(self) -> None:
        self._state = KernelState.CREATED

    @property
    def state(self) -> KernelState:
        return self._state

    def initialize(self) -> None:
        self._state = KernelState.INITIALIZED

    def start(self) -> None:
        self._state = KernelState.RUNNING

    def stop(self) -> None:
        self._state = KernelState.STOPPED

    @property
    def running(self) -> bool:
        return self._state == KernelState.RUNNING
