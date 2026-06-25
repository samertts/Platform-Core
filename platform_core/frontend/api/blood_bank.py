"""
Blood Bank API client for NHDOS Frontend
"""

from dataclasses import dataclass
from .base import BaseEntityClient
from .client import APIClient


@dataclass
class DonationClient(BaseEntityClient):
    """Client for Donation entity API."""
    client: APIClient
    entity_name: str = "donation"
    endpoint: str = "donations"

    def get_by_donor(self, donor_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/donor/{donor_id}")

    def get_by_facility(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")


@dataclass
class BloodUnitClient(BaseEntityClient):
    """Client for BloodUnit entity API."""
    client: APIClient
    entity_name: str = "blood_unit"
    endpoint: str = "blood-units"

    def get_by_blood_type(self, blood_type: str) -> dict:
        return self.client.get(f"{self.endpoint}/blood-type/{blood_type}")

    def get_available(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/available", params={"facility_id": facility_id})

    def get_expiring(self, facility_id: str, days: int = 7) -> dict:
        return self.client.get(f"{self.endpoint}/expiring", params={"facility_id": facility_id, "days": days})

    def crossmatch(self, blood_unit_id: str, patient_id: str) -> dict:
        return self.client.post(f"{self.endpoint}/{blood_unit_id}/crossmatch", data={"patient_id": patient_id})


@dataclass
class TransfusionClient(BaseEntityClient):
    """Client for Transfusion entity API."""
    client: APIClient
    entity_name: str = "transfusion"
    endpoint: str = "transfusions"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_blood_unit(self, blood_unit_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/blood-unit/{blood_unit_id}")

    def record_reaction(self, transfusion_id: str, reaction: str) -> dict:
        return self.client.put(f"{self.endpoint}/{transfusion_id}/reaction", data={"reaction": reaction})
