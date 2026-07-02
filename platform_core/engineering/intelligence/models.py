"""
Platform-Core Engineering Intelligence

Core domain models for the Engineering Intelligence subsystem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .enums import (
    CapabilityState,
    DependencyKind,
    IssueSeverity,
    IssueType,
    KnowledgeSource,
    MetricType,
    RepairStatus,
)

# ---------------------------------------------------------------------
# Repository
# ---------------------------------------------------------------------


@dataclass(slots=True)
class RepositoryFile:
    path: Path
    language: str
    size: int
    checksum: str


@dataclass(slots=True)
class RepositoryModule:
    name: str
    path: Path
    files: list[RepositoryFile] = field(default_factory=list)


@dataclass(slots=True)
class RepositorySnapshot:
    root: Path
    modules: list[RepositoryModule] = field(default_factory=list)


# ---------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------


@dataclass(slots=True)
class IssueLocation:
    file: Path
    line: int
    column: int = 0


@dataclass(slots=True)
class Issue:
    identifier: str

    title: str

    description: str

    severity: IssueSeverity

    issue_type: IssueType

    location: IssueLocation

    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------
# Repair
# ---------------------------------------------------------------------


@dataclass(slots=True)
class RepairAction:
    name: str

    description: str

    automated: bool = True


@dataclass(slots=True)
class RepairPlan:
    identifier: str

    title: str

    actions: list[RepairAction] = field(default_factory=list)


@dataclass(slots=True)
class RepairResult:
    status: RepairStatus

    repaired: int = 0

    skipped: int = 0

    failed: int = 0

    duration: float = 0.0


# ---------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------


@dataclass(slots=True)
class EngineeringMetric:
    name: str

    metric_type: MetricType

    value: float

    maximum: float = 100.0


# ---------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------


@dataclass(slots=True)
class Dependency:
    name: str

    version: str

    kind: DependencyKind


# ---------------------------------------------------------------------
# Capabilities
# ---------------------------------------------------------------------


@dataclass(slots=True)
class Capability:
    identifier: str

    name: str

    state: CapabilityState

    owner: str

    dependencies: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------
# Knowledge
# ---------------------------------------------------------------------


@dataclass(slots=True)
class KnowledgeRecord:
    identifier: str

    title: str

    source: KnowledgeSource

    content: str

    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------
# Learning
# ---------------------------------------------------------------------


@dataclass(slots=True)
class LearningRecord:
    issue: str

    solution: str

    successful: bool

    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------


@dataclass(slots=True)
class ProjectProfile:
    name: str

    version: str

    root: Path

    language: str

    repository: RepositorySnapshot
