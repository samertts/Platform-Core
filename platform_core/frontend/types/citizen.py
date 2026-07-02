"""
Citizen domain types for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntity


@dataclass
class Citizen(BaseEntity):
    """National citizen record."""

    national_id: str = ""
    full_name: str = ""
    date_of_birth: str | None = None
    gender: str | None = None
    blood_type: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    governorate: str | None = None
    district: str | None = None
    status: str = "active"
    confidentiality_level: int = 5


@dataclass
class DigitalCredential(BaseEntity):
    """Digital identity credential."""

    citizen_id: str = ""
    credential_type: str = ""
    credential_number: str = ""
    issue_date: str | None = None
    expiry_date: str | None = None
    issuing_authority: str = ""
    status: str = "active"
    biometric_hash: str | None = None
