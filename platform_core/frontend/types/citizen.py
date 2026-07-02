"""
Citizen domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class Citizen(BaseEntity):
    """National citizen record."""

    national_id: str = ""
    full_name: str = ""
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    governorate: Optional[str] = None
    district: Optional[str] = None
    status: str = "active"
    confidentiality_level: int = 5


@dataclass
class DigitalCredential(BaseEntity):
    """Digital identity credential."""

    citizen_id: str = ""
    credential_type: str = ""
    credential_number: str = ""
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    issuing_authority: str = ""
    status: str = "active"
    biometric_hash: Optional[str] = None
