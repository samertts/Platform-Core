"""
Platform-Core Engineering Intelligence

Exception hierarchy for the Engineering Intelligence subsystem.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ErrorContext:
    """
    Additional structured information attached to an exception.
    """

    component: str
    operation: str
    resource: str | None = None
    details: dict[str, Any] | None = None


class EngineeringError(RuntimeError):
    """
    Base exception for Engineering Intelligence.
    """

    def __init__(
        self,
        message: str,
        *,
        context: ErrorContext | None = None,
    ) -> None:
        super().__init__(message)
        self.context = context


class RepositoryError(EngineeringError):
    """Repository indexing failed."""


class ScannerError(EngineeringError):
    """Repository scanning failed."""


class AnalyzerError(EngineeringError):
    """Analysis stage failed."""


class PlannerError(EngineeringError):
    """Planning stage failed."""


class RepairError(EngineeringError):
    """Automatic repair failed."""


class VerificationError(EngineeringError):
    """Verification failed."""


class KnowledgeError(EngineeringError):
    """Knowledge engine failure."""


class LearningError(EngineeringError):
    """Learning engine failure."""


class ManifestError(EngineeringError):
    """Manifest processing failed."""


class CapabilityError(EngineeringError):
    """Capability registry failure."""


class PluginError(EngineeringError):
    """Plugin execution failed."""


class ConfigurationError(EngineeringError):
    """Configuration is invalid."""


class GitHubIntegrationError(EngineeringError):
    """GitHub integration failed."""


class SecurityViolation(EngineeringError):
    """Security policy violation."""


class GovernanceViolation(EngineeringError):
    """Governance rule violation."""
