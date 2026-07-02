from .state import KernelState


class Lifecycle:

    def __init__(self):

        self._state = KernelState.CREATED

    @property
    def state(self):

        return self._state

    def initialize(self):

        self._state = KernelState.INITIALIZED

    def start(self):

        self._state = KernelState.RUNNING

    def stop(self):

        self._state = KernelState.STOPPED

    @property
    def running(self):

        return self._state == KernelState.RUNNING
