"""
Epidemiology API client for NHDOS Frontend
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class DiseaseClient(BaseEntityClient[Any]):
    """Client for Disease entity API."""

    client: APIClient
    entity_name: str = "disease"
    endpoint: str = "diseases"

    def search(self, query: str, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"q": query}
        if filters:
            params.update(filters)
        return self.client.get(f"{self.endpoint}/search", params=params)

    def get_by_icd(self, icd_code: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/icd/{icd_code}")

    def get_notifiable(self) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/notifiable")


@dataclass
class OutbreakClient(BaseEntityClient[Any]):
    """Client for Outbreak entity API."""

    client: APIClient
    entity_name: str = "outbreak"
    endpoint: str = "outbreaks"

    def get_active(self) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/active")

    def get_by_location(self, location: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/location/{location}")

    def declare(self, outbreak_data: dict[str, Any]) -> dict[str, Any]:
        return self.client.post(f"{self.endpoint}/declare", data=outbreak_data)

    def resolve(self, outbreak_id: str) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{outbreak_id}/resolve")

    def update_cases(self, outbreak_id: str, cases_count: int, deaths_count: int) -> dict[str, Any]:
        return self.client.put(
            f"{self.endpoint}/{outbreak_id}/update-cases",
            data={"cases_count": cases_count, "deaths_count": deaths_count},
        )
