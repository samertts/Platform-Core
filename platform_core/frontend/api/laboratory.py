"""
Laboratory API client for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class SpecimenClient(BaseEntityClient):
    """Client for Specimen entity API."""

    client: APIClient
    entity_name: str = "specimen"
    endpoint: str = "specimens"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def collect(self, specimen_id: str, collector_id: str) -> dict:
        return self.client.put(
            f"{self.endpoint}/{specimen_id}/collect",
            data={"collector_id": collector_id},
        )

    def receive(self, specimen_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{specimen_id}/receive")

    def reject(self, specimen_id: str, reason: str) -> dict:
        return self.client.put(f"{self.endpoint}/{specimen_id}/reject", data={"reason": reason})


@dataclass
class LaboratoryOrderClient(BaseEntityClient):
    """Client for LaboratoryOrder entity API."""

    client: APIClient
    entity_name: str = "laboratory_order"
    endpoint: str = "lab-orders"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_encounter(self, encounter_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/encounter/{encounter_id}")

    def cancel(self, order_id: str, reason: str) -> dict:
        return self.client.put(f"{self.endpoint}/{order_id}/cancel", data={"reason": reason})


@dataclass
class LaboratoryResultClient(BaseEntityClient):
    """Client for LaboratoryResult entity API."""

    client: APIClient
    entity_name: str = "laboratory_result"
    endpoint: str = "lab-results"

    def get_by_order(self, order_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/order/{order_id}")

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def validate(self, result_id: str, validator_id: str) -> dict:
        return self.client.put(
            f"{self.endpoint}/{result_id}/validate", data={"validator_id": validator_id}
        )

    def get_critical_results(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/critical", params={"facility_id": facility_id})


@dataclass
class AnalyzerClient(BaseEntityClient):
    """Client for Analyzer entity API."""

    client: APIClient
    entity_name: str = "analyzer"
    endpoint: str = "analyzers"

    def get_by_facility(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_status(self, analyzer_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{analyzer_id}/status")

    def calibrate(self, analyzer_id: str, calibration_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/{analyzer_id}/calibrate", data=calibration_data)
