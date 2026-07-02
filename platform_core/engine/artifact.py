from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Artifact:
    """
    Immutable description of an artifact produced by an Engine.
    """

    name: str

    path: Path

    kind: str

    size: int | None = None
