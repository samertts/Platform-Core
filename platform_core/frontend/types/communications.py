"""
Communications domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class Correspondence(BaseEntity):
    """Official correspondence record."""

    sender_id: str = ""
    sender_type: str = ""
    recipient_id: str = ""
    recipient_type: str = ""
    subject: str = ""
    body: str = ""
    correspondence_type: str = ""
    priority: str = "normal"
    status: str = "sent"
    read_at: Optional[str] = None
    attachments: list[str] = field(default_factory=list)
    reference_number: Optional[str] = None
