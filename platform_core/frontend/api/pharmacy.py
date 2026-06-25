"""
Pharmacy API client for NHDOS Frontend
"""

from dataclasses import dataclass
from .base import BaseEntityClient
from .client import APIClient


@dataclass
class PrescriptionClient(BaseEntityClient):
    """Client for Prescription entity API."""
    client: APIClient
    entity_name: str = "prescription"
    endpoint: str = "prescriptions"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_encounter(self, encounter_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/encounter/{encounter_id}")

    def cancel(self, prescription_id: str, reason: str) -> dict:
        return self.client.put(f"{self.endpoint}/{prescription_id}/cancel", data={"reason": reason})

    def refill(self, prescription_id: str) -> dict:
        return self.client.post(f"{self.endpoint}/{prescription_id}/refill")


@dataclass
class MedicationClient(BaseEntityClient):
    """Client for Medication entity API."""
    client: APIClient
    entity_name: str = "medication"
    endpoint: str = "medications"

    def search(self, query: str) -> dict:
        return self.client.get(f"{self.endpoint}/search", params={"q": query})

    def get_stock(self, medication_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{medication_id}/stock")

    def update_stock(self, medication_id: str, quantity: int) -> dict:
        return self.client.put(f"{self.endpoint}/{medication_id}/stock", data={"quantity": quantity})

    def get_expiring(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/expiring", params={"facility_id": facility_id})


@dataclass
class DispensingClient(BaseEntityClient):
    """Client for Dispensing entity API."""
    client: APIClient
    entity_name: str = "dispensing"
    endpoint: str = "dispensings"

    def get_by_prescription(self, prescription_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/prescription/{prescription_id}")

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def dispense(self, prescription_id: str, dispensing_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/dispense", data={"prescription_id": prescription_id, **dispensing_data})
