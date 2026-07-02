from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowStarted:
    name: str


@dataclass(frozen=True, slots=True)
class WorkflowCompleted:
    name: str


@dataclass(frozen=True, slots=True)
class WorkflowFailed:
    name: str
