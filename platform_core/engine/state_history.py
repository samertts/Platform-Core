from __future__ import annotations

from dataclasses import dataclass, field

from platform_core.engine.lifecycle import LifecycleState


@dataclass(slots=True)
class StateHistory:
    """
    Records every lifecycle transition performed by an Engine.
    """

    _states: list[LifecycleState] = field(default_factory=list)

    def append(self, state: LifecycleState) -> None:
        self._states.append(state)

    @property
    def states(self) -> tuple[LifecycleState, ...]:
        return tuple(self._states)

    @property
    def last(self) -> LifecycleState | None:
        if not self._states:
            return None

        return self._states[-1]
