"""
Public Health API client for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class VaccineClient(BaseEntityClient):
    """Client for Vaccine entity API."""

    client: APIClient
    entity_name: str = "vaccine"
    endpoint: str = "vaccines"

    def search(self, query: str) -> dict:
        return self.client.get(f"{self.endpoint}/search", params={"q": query})

    def get_by_type(self, vaccine_type: str) -> dict:
        return self.client.get(f"{self.endpoint}/type/{vaccine_type}")


@dataclass
class ImmunizationClient(BaseEntityClient):
    """Client for Immunization entity API."""

    client: APIClient
    entity_name: str = "immunization"
    endpoint: str = "immunizations"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_vaccine(self, vaccine_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/vaccine/{vaccine_id}")

    def record(self, immunization_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/record", data=immunization_data)

    def get_schedule(self, patient_id: str) -> dict:
        return self.client.get(
            f"{self.endpoint}/schedule", params={"patient_id": patient_id}
        )


@dataclass
class ResearchStudyClient(BaseEntityClient):
    """Client for ResearchStudy entity API."""

    client: APIClient
    entity_name: str = "research_study"
    endpoint: str = "research-studies"

    def get_active(self) -> dict:
        return self.client.get(f"{self.endpoint}/active")

    def get_by_facility(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def enroll(self, study_id: str, patient_id: str) -> dict:
        return self.client.post(
            f"{self.endpoint}/{study_id}/enroll", data={"patient_id": patient_id}
        )

    def withdraw(self, study_id: str, patient_id: str, reason: str) -> dict:
        return self.client.put(
            f"{self.endpoint}/{study_id}/withdraw",
            data={"patient_id": patient_id, "reason": reason},
        )
