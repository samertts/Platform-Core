"""
Financial API client for NHDOS Frontend
"""

from dataclasses import dataclass
from .base import BaseEntityClient
from .client import APIClient


@dataclass
class InsuranceClient(BaseEntityClient):
    """Client for Insurance entity API."""
    client: APIClient
    entity_name: str = "insurance"
    endpoint: str = "insurance"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def verify(self, insurance_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{insurance_id}/verify")

    def get_active(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}/active")


@dataclass
class ConsentClient(BaseEntityClient):
    """Client for Consent entity API."""
    client: APIClient
    entity_name: str = "consent"
    endpoint: str = "consents"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def grant(self, consent_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/grant", data=consent_data)

    def revoke(self, consent_id: str, reason: str) -> dict:
        return self.client.put(f"{self.endpoint}/{consent_id}/revoke", data={"reason": reason})

    def check(self, patient_id: str, consent_type: str, target: str) -> dict:
        return self.client.get(f"{self.endpoint}/check", params={"patient_id": patient_id, "type": consent_type, "target": target})


@dataclass
class InvoiceClient(BaseEntityClient):
    """Client for Invoice entity API."""
    client: APIClient
    entity_name: str = "invoice"
    endpoint: str = "invoices"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_facility(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_outstanding(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}/outstanding")

    def mark_paid(self, invoice_id: str, amount: float) -> dict:
        return self.client.put(f"{self.endpoint}/{invoice_id}/paid", data={"amount": amount})


@dataclass
class PaymentClient(BaseEntityClient):
    """Client for Payment entity API."""
    client: APIClient
    entity_name: str = "payment"
    endpoint: str = "payments"

    def get_by_invoice(self, invoice_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/invoice/{invoice_id}")

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def process(self, payment_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/process", data=payment_data)


@dataclass
class ClaimClient(BaseEntityClient):
    """Client for Claim entity API."""
    client: APIClient
    entity_name: str = "claim"
    endpoint: str = "claims"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_insurance(self, insurance_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/insurance/{insurance_id}")

    def submit(self, claim_data: dict) -> dict:
        return self.client.post(f"{self.endpoint}/submit", data=claim_data)

    def approve(self, claim_id: str, approved_amount: float) -> dict:
        return self.client.put(f"{self.endpoint}/{claim_id}/approve", data={"approved_amount": approved_amount})

    def reject(self, claim_id: str, reason: str) -> dict:
        return self.client.put(f"{self.endpoint}/{claim_id}/reject", data={"reason": reason})
