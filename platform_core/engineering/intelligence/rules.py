"""
Engineering Rules
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Rule:

    id: str

    description: str

    enabled: bool = True
