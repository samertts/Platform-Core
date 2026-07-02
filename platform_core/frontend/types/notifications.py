"""
Notifications domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field

from .base import BaseEntity


@dataclass
class Notification(BaseEntity):
    """Notification record."""

    recipient_id: str = ""
    recipient_type: str = ""
    notification_type: str = ""
    title: str = ""
    message: str = ""
    priority: str = "normal"
    status: str = "unread"
    read_at: str | None = None
    channel: str = "in_app"


@dataclass
class Message(BaseEntity):
    """Communication message record."""

    sender_id: str = ""
    sender_type: str = ""
    recipient_id: str = ""
    recipient_type: str = ""
    subject: str | None = None
    body: str = ""
    message_type: str = ""
    status: str = "sent"
    read_at: str | None = None
    attachments: list[str] = field(default_factory=list)
