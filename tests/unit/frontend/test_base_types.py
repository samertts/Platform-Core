"""
Tests for NHDOS Frontend Types
"""

import sys

sys.path.insert(0, "/tmp")

from platform_core.frontend.types.base import (
    ApiResponse,
    BaseEntity,
    BaseEvent,
    BaseRelationship,
    PaginatedResponse,
    PaginationParams,
)


class TestBaseTypes:
    def test_base_entity_creation(self) -> None:
        entity = BaseEntity()
        assert entity.id is not None
        assert entity.version == "1.0.0"
        assert entity.is_active is True

    def test_base_entity_custom_id(self) -> None:
        entity = BaseEntity(id="custom-id-123")
        assert entity.id == "custom-id-123"

    def test_base_relationship_creation(self) -> None:
        rel = BaseRelationship(source_id="s1", target_id="t1")
        assert rel.source_id == "s1"
        assert rel.target_id == "t1"

    def test_base_event_creation(self) -> None:
        event = BaseEvent(event_type="test.event", entity_type="Test", entity_id="e1")
        assert event.event_type == "test.event"
        assert event.entity_type == "Test"

    def test_pagination_params(self) -> None:
        params = PaginationParams(page=2, page_size=10)
        assert params.page == 2
        assert params.page_size == 10

    def test_paginated_response(self) -> None:
        response = PaginatedResponse(items=[1, 2, 3], total=10)
        assert len(response.items) == 3
        assert response.total == 10

    def test_api_response_success(self) -> None:
        response = ApiResponse(success=True, data={"key": "value"})
        assert response.success is True
        assert response.data == {"key": "value"}

    def test_api_response_error(self) -> None:
        response = ApiResponse(success=False, error="Not found")
        assert response.success is False
        assert response.error == "Not found"
