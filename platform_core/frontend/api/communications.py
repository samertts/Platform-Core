"""
Communications API client for NHDOS Frontend
"""

from dataclasses import dataclass
from .base import BaseEntityClient
from .client import APIClient


@dataclass
class CorrespondenceClient(BaseEntityClient):
    """Client for Correspondence entity API."""
    client: APIClient
    entity_name: str = "correspondence"
    endpoint: str = "correspondence"

    def get_by_sender(self, sender_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/sender/{sender_id}")

    def get_by_recipient(self, recipient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/recipient/{recipient_id}")

    def send(self, correspondence_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/send", data=correspondence_data)

    def mark_read(self, correspondence_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{correspondence_id}/read")

    def get_by_type(self, correspondence_type: str) -> dict:
        return self.client.get(f"{self.endpoint}/type/{correspondence_type}")

    def get_by_reference(self, reference_number: str) -> dict:
        return self.client.get(f"{self.endpoint}/reference/{reference_number}")
