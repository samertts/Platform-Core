"""
Healthcare Core API client for NHDOS Frontend
"""

from dataclasses import dataclass
from .base import BaseEntityClient
from .client import APIClient


@dataclass
class PatientClient(BaseEntityClient):
    """Client for Patient entity API."""
    client: APIClient
    entity_name: str = "patient"
    endpoint: str = "patients"

    def get_by_medical_record(self, medical_record_number: str) -> dict:
        return self.client.get(f"{self.endpoint}/medical-record/{medical_record_number}")

    def get_by_citizen(self, citizen_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/citizen/{citizen_id}")

    def get_history(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{patient_id}/history")

    def get_allergies(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{patient_id}/allergies")

    def add_allergy(self, patient_id: str, allergy: str) -> dict:
        return self.client.post(f"{self.endpoint}/{patient_id}/allergies", data={"allergy": allergy})


@dataclass
class VisitClient(BaseEntityClient):
    """Client for Visit entity API."""
    client: APIClient
    entity_name: str = "visit"
    endpoint: str = "visits"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def close(self, visit_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{visit_id}/close")


@dataclass
class EncounterClient(BaseEntityClient):
    """Client for Encounter entity API."""
    client: APIClient
    entity_name: str = "encounter"
    endpoint: str = "encounters"

    def get_by_visit(self, visit_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/visit/{visit_id}")

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def add_note(self, encounter_id: str, note: dict) -> dict:
        return self.client.post(f"{self.endpoint}/{encounter_id}/notes", data=note)

    def complete(self, encounter_id: str, assessment: str, plan: str) -> dict:
        return self.client.put(f"{self.endpoint}/{encounter_id}/complete", data={"assessment": assessment, "plan": plan})


@dataclass
class AppointmentClient(BaseEntityClient):
    """Client for Appointment entity API."""
    client: APIClient
    entity_name: str = "appointment"
    endpoint: str = "appointments"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def get_by_provider(self, provider_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/provider/{provider_id}")

    def confirm(self, appointment_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{appointment_id}/confirm")

    def cancel(self, appointment_id: str, reason: str) -> dict:
        return self.client.put(f"{self.endpoint}/{appointment_id}/cancel", data={"reason": reason})

    def reschedule(self, appointment_id: str, new_date: str, new_time: str) -> dict:
        return self.client.put(f"{self.endpoint}/{appointment_id}/reschedule", data={"date": new_date, "time": new_time})


@dataclass
class AdmissionClient(BaseEntityClient):
    """Client for Admission entity API."""
    client: APIClient
    entity_name: str = "admission"
    endpoint: str = "admissions"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def transfer(self, admission_id: str, new_bed_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{admission_id}/transfer", data={"bed_id": new_bed_id})


@dataclass
class DischargeClient(BaseEntityClient):
    """Client for Discharge entity API."""
    client: APIClient
    entity_name: str = "discharge"
    endpoint: str = "discharges"

    def get_by_admission(self, admission_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/admission/{admission_id}")

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")
