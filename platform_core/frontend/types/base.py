"""
Base types for NHDOS Frontend Domain Model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4


@dataclass
class BaseEntity:
    """Base entity for all NHDOS domain entities."""

    id: str = field(default_factory=lambda: str(uuid4()))
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    is_active: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BaseRelationship:
    """Base relationship between entities."""

    id: str = field(default_factory=lambda: str(uuid4()))
    source_id: str = ""
    target_id: str = ""
    relationship_type: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BaseEvent:
    """Base domain event."""

    id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    entity_type: str = ""
    entity_id: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PaginationParams:
    """Pagination parameters for list queries."""

    page: int = 1
    page_size: int = 20
    sort_by: str = "created_at"
    sort_order: str = "desc"


@dataclass
class PaginatedResponse:
    """Paginated response wrapper."""

    items: list[Any] = field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 20
    total_pages: int = 0


@dataclass
class ApiResponse:
    """Standard API response wrapper."""

    success: bool = True
    data: Any = None
    error: Optional[str] = None
    message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
