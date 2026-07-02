from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EngineWarning:
    message: str
    code: str | None = None
