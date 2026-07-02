"""
Epidemiology API client for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class DiseaseClient(BaseEntityClient):
    """Client for Disease entity API."""

    client: APIClient
    entity_name: str = "disease"
    endpoint: str = "diseases"

    def search(self, query: str) -> dict:
        return self.client.get(f"{self.endpoint}/search", params={"q": query})

    def get_by_icd(self, icd_code: str) -> dict:
        return self.client.get(f"{self.endpoint}/icd/{icd_code}")

    def get_notifiable(self) -> dict:
        return self.client.get(f"{self.endpoint}/notifiable")


@dataclass
class OutbreakClient(BaseEntityClient):
    """Client for Outbreak entity API."""

    client: APIClient
    entity_name: str = "outbreak"
    endpoint: str = "outbreaks"

    def get_active(self) -> dict:
        return self.client.get(f"{self.endpoint}/active")

    def get_by_location(self, location: str) -> dict:
        return self.client.get(f"{self.endpoint}/location/{location}")

    def declare(self, outbreak_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/declare", data=outbreak_data)

    def resolve(self, outbreak_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{outbreak_id}/resolve")

    def update_cases(self, outbreak_id: str, cases_count: int, deaths_count: int) -> dict:
        return self.client.put(
            f"{self.endpoint}/{outbreak_id}/update-cases",
            data={"cases_count": cases_count, "deaths_count": deaths_count},
        )
