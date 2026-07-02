"""
Tests for NHDOS Frontend API Client
"""

import sys

sys.path.insert(0, "/tmp")

from platform_core.frontend.api.base import BaseEntityClient
from platform_core.frontend.api.client import APIClient, APIConfig, APIError


class TestAPIClient:
    def test_client_creation(self):
        client = APIClient()
        assert client.config.base_url == "http://localhost:8000"

    def test_client_custom_config(self):
        config = APIConfig(base_url="http://custom:9000", auth_token="test-token")
        client = APIClient(config=config)
        assert client.config.base_url == "http://custom:9000"
        assert client.config.auth_token == "test-token"

    def test_client_build_url(self):
        client = APIClient()
        url = client._build_url("patients")
        assert url == "http://localhost:8000/api/v1/patients"

    def test_client_health_check(self):
        client = APIClient()
        result = client.health_check()
        assert result["success"] is True

    def test_client_get(self):
        client = APIClient()
        result = client.get("patients")
        assert result["success"] is True

    def test_client_post(self):
        client = APIClient()
        result = client.post("patients", data={"name": "test"})
        assert result["success"] is True

    def test_client_put(self):
        client = APIClient()
        result = client.put("patients/123", data={"name": "updated"})
        assert result["success"] is True

    def test_client_delete(self):
        client = APIClient()
        result = client.delete("patients/123")
        assert result["success"] is True


class TestBaseEntityClient:
    def test_entity_client_creation(self):
        client = APIClient()
        entity_client = BaseEntityClient(
            client=client, entity_name="patient", endpoint="patients"
        )
        assert entity_client.entity_name == "patient"
        assert entity_client.endpoint == "patients"

    def test_entity_client_list(self):
        client = APIClient()
        entity_client = BaseEntityClient(
            client=client, entity_name="patient", endpoint="patients"
        )
        result = entity_client.list()
        assert result["success"] is True

    def test_entity_client_get(self):
        client = APIClient()
        entity_client = BaseEntityClient(
            client=client, entity_name="patient", endpoint="patients"
        )
        result = entity_client.get("123")
        assert result["success"] is True

    def test_entity_client_create(self):
        client = APIClient()
        entity_client = BaseEntityClient(
            client=client, entity_name="patient", endpoint="patients"
        )
        result = entity_client.create({"name": "test"})
        assert result["success"] is True

    def test_entity_client_update(self):
        client = APIClient()
        entity_client = BaseEntityClient(
            client=client, entity_name="patient", endpoint="patients"
        )
        result = entity_client.update("123", {"name": "updated"})
        assert result["success"] is True

    def test_entity_client_delete(self):
        client = APIClient()
        entity_client = BaseEntityClient(
            client=client, entity_name="patient", endpoint="patients"
        )
        result = entity_client.delete("123")
        assert result["success"] is True


class TestAPIError:
    def test_api_error_creation(self):
        error = APIError("Test error", status_code=404, details={"key": "value"})
        assert str(error) == "Test error"
        assert error.status_code == 404
        assert error.details == {"key": "value"}
