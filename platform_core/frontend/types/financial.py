"""
Financial domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field

from .base import BaseEntity


@dataclass
class Insurance(BaseEntity):
    """Insurance record."""

    patient_id: str = ""
    insurance_provider: str = ""
    policy_number: str = ""
    group_number: str | None = None
    coverage_type: str = ""
    start_date: str = ""
    end_date: str | None = None
    status: str = "active"


@dataclass
class Consent(BaseEntity):
    """Patient consent record."""

    patient_id: str = ""
    consent_type: str = ""
    consent_date: str = ""
    expiry_date: str | None = None
    scope: str = ""
    granted_to: list[str] = field(default_factory=list)
    status: str = "active"
    withdrawal_date: str | None = None


@dataclass
class Invoice(BaseEntity):
    """Financial invoice record."""

    patient_id: str = ""
    facility_id: str = ""
    invoice_number: str = ""
    invoice_date: str = ""
    due_date: str | None = None
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
    reference_number: str | None = None
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
    approved_amount: float | None = None
    status: str = "submitted"
    denial_reason: str | None = None
