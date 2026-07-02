"""
Clinical API client for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class DiagnosisClient(BaseEntityClient):
    """Client for Diagnosis entity API."""

    client: APIClient
    entity_name: str = "diagnosis"
    endpoint: str = "diagnoses"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_encounter(self, encounter_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/encounter/{encounter_id}")

    def confirm(self, diagnosis_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{diagnosis_id}/confirm")

    def resolve(self, diagnosis_id: str, resolution_date: str) -> dict:
        return self.client.put(
            f"{self.endpoint}/{diagnosis_id}/resolve",
            data={"resolution_date": resolution_date},
        )


@dataclass
class ProcedureClient(BaseEntityClient):
    """Client for Procedure entity API."""

    client: APIClient
    entity_name: str = "procedure"
    endpoint: str = "procedures"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_encounter(self, encounter_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/encounter/{encounter_id}")

    def complete(self, procedure_id: str, notes: str) -> dict:
        return self.client.put(f"{self.endpoint}/{procedure_id}/complete", data={"notes": notes})


@dataclass
class ObservationClient(BaseEntityClient):
    """Client for Observation entity API."""

    client: APIClient
    entity_name: str = "observation"
    endpoint: str = "observations"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_encounter(self, encounter_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/encounter/{encounter_id}")

    def record(self, observation_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/record", data=observation_data)


@dataclass
class VitalSignsClient(BaseEntityClient):
    """Client for VitalSigns entity API."""

    client: APIClient
    entity_name: str = "vital_signs"
    endpoint: str = "vital-signs"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_encounter(self, encounter_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/encounter/{encounter_id}")

    def record(self, vitals_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/record", data=vitals_data)

    def get_trends(self, patient_id: str, vital_type: str, days: int = 30) -> dict:
        return self.client.get(
            f"{self.endpoint}/trends",
            params={"patient_id": patient_id, "vital_type": vital_type, "days": days},
        )
