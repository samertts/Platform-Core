"""
Citizen API client for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class CitizenClient(BaseEntityClient):
    """Client for Citizen entity API."""

    client: APIClient
    entity_name: str = "citizen"
    endpoint: str = "citizens"

    def get_by_national_id(self, national_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/national-id/{national_id}")

    def verify_identity(self, citizen_id: str, verification_data: dict) -> dict:
        return self.client.post(
            f"{self.endpoint}/{citizen_id}/verify", data=verification_data
        )

    def suspend(self, citizen_id: str, reason: str) -> dict:
        return self.client.put(
            f"{self.endpoint}/{citizen_id}/suspend", data={"reason": reason}
        )

    def reactivate(self, citizen_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{citizen_id}/reactivate")


@dataclass
class DigitalCredentialClient(BaseEntityClient):
    """Client for DigitalCredential entity API."""

    client: APIClient
    entity_name: str = "digital_credential"
    endpoint: str = "digital-credentials"

    def get_by_citizen(self, citizen_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/citizen/{citizen_id}")

    def issue(self, data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/issue", data=data)

    def revoke(self, credential_id: str, reason: str) -> dict:
        return self.client.put(
            f"{self.endpoint}/{credential_id}/revoke", data={"reason": reason}
        )

    def verify(self, credential_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{credential_id}/verify")
