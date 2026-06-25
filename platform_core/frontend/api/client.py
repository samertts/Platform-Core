"""
Base API client for NHDOS Frontend
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, TypeVar, Generic
from uuid import uuid4
import json

T = TypeVar("T")


class APIError(Exception):
    """API error exception."""
    def __init__(self, message: str, status_code: int = 500, details: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}


@dataclass
class APIConfig:
    """API configuration."""
    base_url: str = "http://localhost:8000"
    api_version: str = "v1"
    timeout: int = 30
    retry_count: int = 3
    auth_token: Optional[str] = None
    headers: dict[str, str] = field(default_factory=dict)


@dataclass
class APIClient:
    """Main API client for NHDOS platform."""
    config: APIConfig = field(default_factory=APIConfig)
    _session: Any = None

    def __post_init__(self):
        if self.config.auth_token:
            self.config.headers["Authorization"] = f"Bearer {self.config.auth_token}"
        self.config.headers["Content-Type"] = "application/json"
        self.config.headers["Accept"] = "application/json"

    def _build_url(self, endpoint: str) -> str:
        return f"{self.config.base_url}/api/{self.config.api_version}/{endpoint}"

    def _make_request(self, method: str, endpoint: str, data: Optional[dict] = None, params: Optional[dict] = None) -> dict:
        url = self._build_url(endpoint)
        try:
            return {"success": True, "data": {}, "timestamp": datetime.utcnow().isoformat()}
        except Exception as e:
            raise APIError(f"Request failed: {str(e)}", 500)

    def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[dict] = None) -> dict:
        return self._make_request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Optional[dict] = None) -> dict:
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> dict:
        return self._make_request("DELETE", endpoint)

    def health_check(self) -> dict:
        return self.get("health")
