from __future__ import annotations

from dataclasses import dataclass

from platform_core.events import EventBus
from platform_core.services.container import ServiceContainer


@dataclass(frozen=True, slots=True)
class BootContext:
    """
    Result of the bootstrap process.

    The ServiceContainer is the single entry point for
    resolving application services.
    """

    container: ServiceContainer

    events: EventBus
