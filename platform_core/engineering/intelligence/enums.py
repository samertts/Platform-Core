"""
Platform-Core Engineering Intelligence

Central enumerations used across the Engineering Intelligence
subsystem.

This module intentionally contains no business logic.
It provides stable enums shared by scanners, analyzers,
repair engines, planners, repositories, plugins,
knowledge providers and orchestration components.
"""

from __future__ import annotations

from enum import StrEnum, auto


class IssueSeverity(StrEnum):
    """Engineering issue severity."""

    INFO = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


class IssueType(StrEnum):
    """Engineering issue classification."""

    STYLE = auto()
    BUG = auto()
    SECURITY = auto()
    TEST = auto()
    ARCHITECTURE = auto()
    DOCUMENTATION = auto()
    DEPENDENCY = auto()
    PERFORMANCE = auto()
    COMPATIBILITY = auto()
    DUPLICATION = auto()
    DEAD_CODE = auto()
    GOVERNANCE = auto()
    CONFIGURATION = auto()
    RUNTIME = auto()
    MANIFEST = auto()
    PLUGIN = auto()


class RepositoryObject(StrEnum):
    """Repository object types."""

    PROJECT = auto()
    PACKAGE = auto()
    MODULE = auto()
    CLASS = auto()
    FUNCTION = auto()
    METHOD = auto()
    FILE = auto()
    DIRECTORY = auto()
    TEST = auto()
    PLUGIN = auto()
    CAPABILITY = auto()
    MANIFEST = auto()
    KNOWLEDGE = auto()


class CapabilityState(StrEnum):
    """Capability lifecycle."""

    ENABLED = auto()
    DISABLED = auto()
    EXPERIMENTAL = auto()
    DEPRECATED = auto()
    REMOVED = auto()


class RepairStatus(StrEnum):
    """Repair execution state."""

    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    SKIPPED = auto()
    ROLLED_BACK = auto()


class ScanStatus(StrEnum):
    """Repository scan state."""

    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()


class KnowledgeSource(StrEnum):
    """Knowledge origin."""

    LOCAL = auto()
    GENERATED = auto()
    DOCUMENTATION = auto()
    GITHUB = auto()
    PLUGIN = auto()
    USER = auto()


class ExecutionMode(StrEnum):
    """Execution strategy."""

    READ_ONLY = auto()
    ANALYSIS = auto()
    REPAIR = auto()
    VERIFY = auto()
    AUTONOMOUS = auto()


class MetricType(StrEnum):
    """Engineering metrics."""

    QUALITY = auto()
    SECURITY = auto()
    TESTING = auto()
    PERFORMANCE = auto()
    MAINTAINABILITY = auto()
    COMPLEXITY = auto()
    RELIABILITY = auto()
    COVERAGE = auto()


class DependencyKind(StrEnum):
    """Dependency classification."""

    PYTHON = auto()
    SYSTEM = auto()
    CONTAINER = auto()
    PLUGIN = auto()
    SERVICE = auto()
    TOOL = auto()


class LearningEvent(StrEnum):
    """Learning event types."""

    ISSUE_FOUND = auto()
    ISSUE_FIXED = auto()
    REPAIR_FAILED = auto()
    TEST_FAILED = auto()
    TEST_PASSED = auto()
    ARCHITECTURE_UPDATED = auto()
    KNOWLEDGE_ADDED = auto()
