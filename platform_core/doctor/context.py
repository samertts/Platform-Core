from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DoctorContext:
    """
    Input for DoctorEngine.
    """

    project_root: Path

    strict: bool = False

    fix: bool = False

    include: tuple[str, ...] = ()

    exclude: tuple[str, ...] = ()

    variables: dict[str, str] = field(default_factory=dict)
