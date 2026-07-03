"""Knowledge Graph Engine - Core Types.

All enums, dataclasses, and type definitions for the Knowledge Graph.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

# ---------------------------------------------------------------------------
# Node Types
# ---------------------------------------------------------------------------


class NodeType(StrEnum):
    REPOSITORY = "repository"
    MODULE = "module"
    SERVICE = "service"
    API = "api"
    EVENT = "event"
    PACKAGE = "package"
    PLUGIN = "plugin"
    SDK = "sdk"
    WORKFLOW = "workflow"
    POLICY = "policy"
    DEVICE = "device"
    DRIVER = "driver"
    PROTOCOL = "protocol"
    DATABASE = "database"
    INFRASTRUCTURE = "infrastructure"
    HEALTHCARE_STANDARD = "healthcare_standard"
    USER_ROLE = "user_role"
    CERTIFICATION = "certification"
    RISK = "risk"
    ISSUE = "issue"
    DEPLOYMENT = "deployment"
    ENVIRONMENT = "environment"


class NodeStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    PENDING = "pending"
    DRAFT = "draft"
    RETIRED = "retired"


class LifecycleStage(StrEnum):
    IDEA = "idea"
    PLANNING = "planning"
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"


# ---------------------------------------------------------------------------
# Relationship Types
# ---------------------------------------------------------------------------


class RelationshipType(StrEnum):
    DEPENDS_ON = "depends_on"
    USES = "uses"
    IMPLEMENTS = "implements"
    EXPOSES = "exposes"
    GENERATES = "generates"
    CONSUMES = "consumes"
    PUBLISHES = "publishes"
    SUBSCRIBES = "subscribes"
    CONNECTS_TO = "connects_to"
    HOSTED_ON = "hosted_on"
    CERTIFIED_BY = "certified_by"
    GOVERNED_BY = "governed_by"
    REQUIRES = "requires"
    EXTENDS = "extends"
    INHERITS = "inherits"
    REPLACES = "replaces"
    SUPERSEDES = "supersedes"
    MIGRATES_TO = "migrates_to"
    SUPPORTED_BY = "supported_by"
    COMPATIBLE_WITH = "compatible_with"
    INCOMPATIBLE_WITH = "incompatible_with"


class RelationshipStatus(StrEnum):
    ACTIVE = "active"
    PROPOSED = "proposed"
    DEPRECATED = "deprecated"
    BROKEN = "broken"
    SUSPENDED = "suspended"


# ---------------------------------------------------------------------------
# Query Types
# ---------------------------------------------------------------------------


class QueryType(StrEnum):
    DEPENDENCY_ANALYSIS = "dependency_analysis"
    IMPACT_ANALYSIS = "impact_analysis"
    CIRCULAR_DEPENDENCY = "circular_dependency"
    SHORTEST_PATH = "shortest_path"
    REACHABILITY = "reachability"
    MODULE_OWNERSHIP = "module_ownership"
    ARCHITECTURE_NAVIGATION = "architecture_navigation"
    RISK_PROPAGATION = "risk_propagation"
    PACKAGE_COMPATIBILITY = "package_compatibility"
    HEALTHCARE_USAGE = "healthcare_usage"
    REPOSITORY_HEALTH = "repository_health"
    CERTIFICATION_STATUS = "certification_status"


# ---------------------------------------------------------------------------
# Impact Types
# ---------------------------------------------------------------------------


class ImpactLevel(StrEnum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ChangeType(StrEnum):
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"
    DEPRECATE = "deprecate"
    REPLACE = "replace"
    MIGRATE = "migrate"


# ---------------------------------------------------------------------------
# Architecture Intelligence Types
# ---------------------------------------------------------------------------


class SmellType(StrEnum):
    ORPHAN_SERVICE = "orphan_service"
    DEAD_MODULE = "dead_module"
    UNUSED_API = "unused_api"
    DUPLICATE_SERVICE = "duplicate_service"
    CIRCULAR_DEPENDENCY = "circular_dependency"
    HIGH_COUPLING = "high_coupling"
    LOW_COHESION = "low_cohesion"
    GOVERNANCE_VIOLATION = "governance_violation"
    GOD_MODULE = "god_module"
    FEATURE_ENVY = "feature_envy"
    DATA_LOBSTER = "data_lobster"
    SHOTGUN_SURGERY = "shotgun_surgery"


class RecommendationPriority(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


# ---------------------------------------------------------------------------
# Healthcare Types
# ---------------------------------------------------------------------------


class HealthcareStandard(StrEnum):
    HL7 = "hl7"
    FHIR = "fhir"
    LOINC = "loinc"
    SNOMED_CT = "snomed_ct"
    ICD = "icd"
    ASTM = "astm"
    DICOM = "dicom"
    IHE = "ihe"
    HL7_V2 = "hl7_v2"
    HL7_V3 = "hl7_v3"
    CDA = "cda"
    X12 = "x12"


class HealthcareEntity(StrEnum):
    LABORATORY_EQUIPMENT = "laboratory_equipment"
    ANALYZER = "analyzer"
    MEDICAL_DEVICE = "medical_device"
    HEALTHCARE_WORKFLOW = "healthcare_workflow"
    HEALTHCARE_REGULATION = "healthcare_regulation"
    LABORATORY_STANDARD = "laboratory_standard"
    PATIENT_RECORD = "patient_record"
    CLINICAL_DOCUMENT = "clinical_document"


# ---------------------------------------------------------------------------
# Temporal Types
# ---------------------------------------------------------------------------


class EventType(StrEnum):
    NODE_CREATED = "node_created"
    NODE_UPDATED = "node_updated"
    NODE_DELETED = "node_deleted"
    NODE_STATUS_CHANGED = "node_status_changed"
    RELATIONSHIP_CREATED = "relationship_created"
    RELATIONSHIP_UPDATED = "relationship_updated"
    RELATIONSHIP_DELETED = "relationship_deleted"
    SNAPSHOT_CREATED = "snapshot_created"
    SNAPSHOT_RESTORED = "snapshot_restored"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------


@dataclass
class Node:
    """A node in the knowledge graph."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_type: NodeType = NodeType.MODULE
    name: str = ""
    version: str = "1.0.0"
    metadata: dict[str, Any] = field(default_factory=dict)
    lifecycle: LifecycleStage = LifecycleStage.DEVELOPMENT
    owner: str = ""
    status: NodeStatus = NodeStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    labels: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "node_type": self.node_type.value,
            "name": self.name,
            "version": self.version,
            "metadata": self.metadata,
            "lifecycle": self.lifecycle.value,
            "owner": self.owner,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "labels": self.labels,
            "tags": self.tags,
            "capabilities": self.capabilities,
        }


@dataclass
class Edge:
    """A relationship edge in the knowledge graph."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str = ""
    target_id: str = ""
    relationship_type: RelationshipType = RelationshipType.DEPENDS_ON
    status: RelationshipStatus = RelationshipStatus.ACTIVE
    version: str = "1.0.0"
    validity: str = "valid"
    confidence: float = 1.0
    source_origin: str = ""
    evidence: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type.value,
            "status": self.status.value,
            "version": self.version,
            "validity": self.validity,
            "confidence": self.confidence,
            "source_origin": self.source_origin,
            "evidence": self.evidence,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class GraphSnapshot:
    """A point-in-time snapshot of the graph."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    description: str = ""
    node_count: int = 0
    edge_count: int = 0
    nodes_snapshot: dict[str, dict[str, Any]] = field(default_factory=dict)
    edges_snapshot: dict[str, dict[str, Any]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TemporalEvent:
    """An event in the temporal history."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.NODE_CREATED
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    entity_id: str = ""
    entity_type: NodeType | RelationshipType | None = None
    old_value: dict[str, Any] | None = None
    new_value: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryResult:
    """Result from a graph query."""

    query_type: QueryType = QueryType.DEPENDENCY_ANALYSIS
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    paths: list[list[str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0


@dataclass
class ImpactReport:
    """Impact analysis report."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    change_type: ChangeType = ChangeType.MODIFY
    source_node_id: str = ""
    impact_level: ImpactLevel = ImpactLevel.NONE
    affected_repositories: list[str] = field(default_factory=list)
    affected_services: list[str] = field(default_factory=list)
    affected_apis: list[str] = field(default_factory=list)
    affected_events: list[str] = field(default_factory=list)
    affected_devices: list[str] = field(default_factory=list)
    affected_workflows: list[str] = field(default_factory=list)
    affected_packages: list[str] = field(default_factory=list)
    affected_standards: list[str] = field(default_factory=list)
    affected_deployments: list[str] = field(default_factory=list)
    total_affected: int = 0
    recommendations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class ArchitectureSmell:
    """An architectural smell detected by the intelligence engine."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    smell_type: SmellType = SmellType.ORPHAN_SERVICE
    description: str = ""
    affected_nodes: list[str] = field(default_factory=list)
    severity: ImpactLevel = ImpactLevel.MEDIUM
    recommendation: str = ""
    detected_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ArchitectureRecommendation:
    """A recommendation from architecture intelligence."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    priority: RecommendationPriority = RecommendationPriority.MEDIUM
    title: str = ""
    description: str = ""
    affected_nodes: list[str] = field(default_factory=list)
    estimated_effort: str = ""
    rationale: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthcareMapping:
    """Mapping between a graph node and a healthcare standard."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_id: str = ""
    standard: HealthcareStandard = HealthcareStandard.FHIR
    entity_type: HealthcareEntity = HealthcareEntity.CLINICAL_DOCUMENT
    code: str = ""
    display_name: str = ""
    version: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AIReasoningResult:
    """Result from AI reasoning layer."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reasoning_type: str = ""
    question: str = ""
    answer: str = ""
    confidence: float = 0.0
    supporting_nodes: list[str] = field(default_factory=list)
    supporting_edges: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class GraphVisualization:
    """A graph visualization output."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    graph_type: str = ""
    nodes: list[dict[str, Any]] = field(default_factory=list)
    edges: list[dict[str, Any]] = field(default_factory=list)
    layout: str = "force_directed"
    metadata: dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "graph_type": self.graph_type,
            "nodes": self.nodes,
            "edges": self.edges,
            "layout": self.layout,
            "metadata": self.metadata,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class KnowledgeEngineConfig:
    """Configuration for the Knowledge Engine."""

    max_nodes: int = 100000
    max_edges: int = 500000
    enable_temporal: bool = True
    enable_ai: bool = True
    enable_healthcare: bool = True
    snapshot_interval: int = 100
    cache_size: int = 10000
    thread_safe: bool = True
    immutable_history: bool = True


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class KnowledgeError(Exception):
    """Base exception for knowledge graph operations."""


class NodeNotFoundError(KnowledgeError):
    """Raised when a node is not found."""


class EdgeNotFoundError(KnowledgeError):
    """Raised when an edge is not found."""


class CircularDependencyError(KnowledgeError):
    """Raised when a circular dependency is detected."""


class GraphConstraintError(KnowledgeError):
    """Raised when a graph constraint is violated."""


class TemporalError(KnowledgeError):
    """Raised for temporal graph errors."""
