"""
Public Health API client for NHDOS Frontend
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class VaccineClient(BaseEntityClient[Any]):
    """Client for Vaccine entity API."""

    client: APIClient
    entity_name: str = "vaccine"
    endpoint: str = "vaccines"

    def search(self, query: str, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"q": query}
        if filters:
            params.update(filters)
        return self.client.get(f"{self.endpoint}/search", params=params)

    def get_by_type(self, vaccine_type: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/type/{vaccine_type}")


@dataclass
class ImmunizationClient(BaseEntityClient[Any]):
    """Client for Immunization entity API."""

    client: APIClient
    entity_name: str = "immunization"
    endpoint: str = "immunizations"

    def get_by_patient(self, patient_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_vaccine(self, vaccine_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/vaccine/{vaccine_id}")

    def record(self, immunization_data: dict[str, Any]) -> dict[str, Any]:
        return self.client.post(f"{self.endpoint}/record", data=immunization_data)

    def get_schedule(self, patient_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/schedule", params={"patient_id": patient_id})


@dataclass
class ResearchStudyClient(BaseEntityClient[Any]):
    """Client for ResearchStudy entity API."""

    client: APIClient
    entity_name: str = "research_study"
    endpoint: str = "research-studies"

    def get_active(self) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/active")

    def get_by_facility(self, facility_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def enroll(self, study_id: str, patient_id: str) -> dict[str, Any]:
        return self.client.post(
            f"{self.endpoint}/{study_id}/enroll", data={"patient_id": patient_id}
        )

    def withdraw(self, study_id: str, patient_id: str, reason: str) -> dict[str, Any]:
        return self.client.put(
            f"{self.endpoint}/{study_id}/withdraw",
            data={"patient_id": patient_id, "reason": reason},
        )
