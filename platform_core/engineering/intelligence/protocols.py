"""
Platform-Core Engineering Intelligence

Protocols (Contracts) for Engineering Intelligence.

All scanners, analyzers, planners, repair engines,
knowledge providers and repository providers must
implement these interfaces.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol
from typing import Iterable
from typing import runtime_checkable

from .models import (
    Capability,
    Dependency,
    EngineeringMetric,
    Issue,
    KnowledgeRecord,
    ProjectProfile,
    RepairPlan,
    RepairResult,
    RepositorySnapshot,
)


# ============================================================
# Repository
# ============================================================


@runtime_checkable
class RepositoryProviderProtocol(Protocol):

    def load(self, root: Path) -> RepositorySnapshot:
        ...

    def refresh(self) -> RepositorySnapshot:
        ...


# ============================================================
# Scanner
# ============================================================


@runtime_checkable
class ScannerProtocol(Protocol):

    def scan(self, root: Path) -> RepositorySnapshot:
        ...


# ============================================================
# Analyzer
# ============================================================


@runtime_checkable
class AnalyzerProtocol(Protocol):

    def analyze(
        self,
        repository: RepositorySnapshot,
    ) -> list[Issue]:
        ...


# ============================================================
# Planner
# ============================================================


@runtime_checkable
class PlannerProtocol(Protocol):

    def build_plan(
        self,
        issues: list[Issue],
    ) -> RepairPlan:
        ...


# ============================================================
# Repair
# ============================================================


@runtime_checkable
class RepairEngineProtocol(Protocol):

    def repair(
        self,
        plan: RepairPlan,
    ) -> RepairResult:
        ...


# ============================================================
# Knowledge
# ============================================================


@runtime_checkable
class KnowledgeProviderProtocol(Protocol):

    def search(
        self,
        query: str,
    ) -> Iterable[KnowledgeRecord]:
        ...

    def learn(
        self,
        record: KnowledgeRecord,
    ) -> None:
        ...


# ============================================================
# Metrics
# ============================================================


@runtime_checkable
class MetricsProviderProtocol(Protocol):

    def collect(self) -> list[EngineeringMetric]:
        ...


# ============================================================
# Capability Registry
# ============================================================


@runtime_checkable
class CapabilityRegistryProtocol(Protocol):

    def list(self) -> list[Capability]:
        ...

    def get(
        self,
        identifier: str,
    ) -> Capability:
        ...


# ============================================================
# Dependency Provider
# ============================================================


@runtime_checkable
class DependencyProviderProtocol(Protocol):

    def dependencies(self) -> list[Dependency]:
        ...


# ============================================================
# Project
# ============================================================


@runtime_checkable
class ProjectProviderProtocol(Protocol):

    def profile(self) -> ProjectProfile:
        ...
