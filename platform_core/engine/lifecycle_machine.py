from __future__ import annotations

from platform_core.engine.lifecycle import LifecycleState
from platform_core.engine.state_history import StateHistory


_ALLOWED_TRANSITIONS: dict[LifecycleState, set[LifecycleState]] = {
    LifecycleState.CREATED: {
        LifecycleState.CONFIGURED,
    },
    LifecycleState.CONFIGURED: {
        LifecycleState.INITIALIZED,
    },
    LifecycleState.INITIALIZED: {
        LifecycleState.READY,
    },
    LifecycleState.READY: {
        LifecycleState.RUNNING,
    },
    LifecycleState.RUNNING: {
        LifecycleState.COMPLETED,
        LifecycleState.FAILED,
        LifecycleState.CANCELLED,
    },
    LifecycleState.COMPLETED: {
        LifecycleState.DISPOSED,
    },
    LifecycleState.FAILED: {
        LifecycleState.DISPOSED,
    },
    LifecycleState.CANCELLED: {
        LifecycleState.DISPOSED,
    },
    LifecycleState.DISPOSED: set(),
}


class LifecycleMachine:
    """
    Owns the Engine lifecycle state machine.

    BaseEngine MUST delegate every lifecycle transition to this object.
    """

    def __init__(self) -> None:

        self._state = LifecycleState.CREATED

        self._history = StateHistory()

        self._history.append(self._state)

    @property
    def state(self) -> LifecycleState:
        return self._state

    @property
    def history(self) -> tuple[LifecycleState, ...]:
        return self._history.states

    def transition(self, target: LifecycleState) -> None:

        allowed = _ALLOWED_TRANSITIONS[self._state]

        if target not in allowed:

            raise RuntimeError(
                f"Illegal lifecycle transition "
                f"{self._state.value} -> {target.value}"
            )

        self._state = target

        self._history.append(target)

    def configure(self) -> None:
        self.transition(LifecycleState.CONFIGURED)

    def initialize(self) -> None:
        self.transition(LifecycleState.INITIALIZED)

    def ready(self) -> None:
        self.transition(LifecycleState.READY)

    def running(self) -> None:
        self.transition(LifecycleState.RUNNING)

    def completed(self) -> None:
        self.transition(LifecycleState.COMPLETED)

    def failed(self) -> None:
        self.transition(LifecycleState.FAILED)

    def cancelled(self) -> None:
        self.transition(LifecycleState.CANCELLED)

    def disposed(self) -> None:
        self.transition(LifecycleState.DISPOSED)
