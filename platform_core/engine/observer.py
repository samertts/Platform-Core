from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from platform_core.engine.events import EngineEvent


class EngineObserver(ABC):
    """
    Receives every EngineEvent.

    Logging, Metrics, Tracing and Progress reporting
    are all observers.
    """

    @abstractmethod
    def notify(
        self,
        event: EngineEvent,
    ) -> None:
        ...
