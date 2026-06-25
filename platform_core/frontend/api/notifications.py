"""
Notifications API client for NHDOS Frontend
"""

from dataclasses import dataclass
from .base import BaseEntityClient
from .client import APIClient


@dataclass
class NotificationClient(BaseEntityClient):
    """Client for Notification entity API."""
    client: APIClient
    entity_name: str = "notification"
    endpoint: str = "notifications"

    def get_by_recipient(self, recipient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/recipient/{recipient_id}")

    def get_unread(self, recipient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/unread", params={"recipient_id": recipient_id})

    def mark_read(self, notification_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{notification_id}/read")

    def mark_all_read(self, recipient_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/read-all", data={"recipient_id": recipient_id})

    def send(self, notification_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/send", data=notification_data)


@dataclass
class MessageClient(BaseEntityClient):
    """Client for Message entity API."""
    client: APIClient
    entity_name: str = "message"
    endpoint: str = "messages"

    def get_by_sender(self, sender_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/sender/{sender_id}")

    def get_by_recipient(self, recipient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/recipient/{recipient_id}")

    def send(self, message_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/send", data=message_data)

    def mark_read(self, message_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{message_id}/read")

    def get_conversation(self, user1_id: str, user2_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/conversation", params={"user1": user1_id, "user2": user2_id})
