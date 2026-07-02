from __future__ import annotations

from dataclasses import dataclass

from platform_core.events import EventBus
from platform_core.kernel.kernel import Kernel
from platform_core.services.container import ServiceContainer


@dataclass(frozen=True, slots=True)
class RuntimeContext:
    """
    Runtime state exposed by the ApplicationHost.
    """

    kernel: Kernel

    container: ServiceContainer

    events: EventBus
