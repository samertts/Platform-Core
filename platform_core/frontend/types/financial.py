"""
Financial domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class Insurance(BaseEntity):
    """Insurance record."""

    patient_id: str = ""
    insurance_provider: str = ""
    policy_number: str = ""
    group_number: Optional[str] = None
    coverage_type: str = ""
    start_date: str = ""
    end_date: Optional[str] = None
    status: str = "active"


@dataclass
class Consent(BaseEntity):
    """Patient consent record."""

    patient_id: str = ""
    consent_type: str = ""
    consent_date: str = ""
    expiry_date: Optional[str] = None
    scope: str = ""
    granted_to: list[str] = field(default_factory=list)
    status: str = "active"
    withdrawal_date: Optional[str] = None


@dataclass
class Invoice(BaseEntity):
    """Financial invoice record."""

    patient_id: str = ""
    facility_id: str = ""
    invoice_number: str = ""
    invoice_date: str = ""
    due_date: Optional[str] = None
    total_amount: float = 0.0
    paid_amount: float = 0.0
    currency: str = "IQD"
    status: str = "pending"


@dataclass
class Payment(BaseEntity):
    """Payment record."""

    invoice_id: str = ""
    patient_id: str = ""
    payment_date: str = ""
    amount: float = 0.0
    currency: str = "IQD"
    payment_method: str = ""
    reference_number: Optional[str] = None
    status: str = "completed"


@dataclass
class Claim(BaseEntity):
    """Insurance claim record."""

    patient_id: str = ""
    insurance_id: str = ""
    invoice_id: str = ""
    claim_number: str = ""
    claim_date: str = ""
    claim_amount: float = 0.0
    approved_amount: Optional[float] = None
    status: str = "submitted"
    denial_reason: Optional[str] = None
