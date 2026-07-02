from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScheduledTask:
    name: str

    action: Callable[[], None]
