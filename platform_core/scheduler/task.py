from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, slots=True)
class ScheduledTask:

    name: str

    action: Callable[[], None]
