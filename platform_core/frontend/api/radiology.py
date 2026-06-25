"""
Radiology API client for NHDOS Frontend
"""

from dataclasses import dataclass
from .base import BaseEntityClient
from .client import APIClient


@dataclass
class RadiologyStudyClient(BaseEntityClient):
    """Client for RadiologyStudy entity API."""
    client: APIClient
    entity_name: str = "radiology_study"
    endpoint: str = "radiology-studies"

    def get_by_patient(self, patient_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/patient/{patient_id}")

    def schedule(self, study_id: str, schedule_data: dict) -> dict:
        return self.client.put(f"{self.endpoint}/{study_id}/schedule", data=schedule_data)

    def complete(self, study_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{study_id}/complete")


@dataclass
class ImageClient(BaseEntityClient):
    """Client for Image entity API."""
    client: APIClient
    entity_name: str = "image"
    endpoint: str = "images"

    def get_by_study(self, study_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/study/{study_id}")

    def download(self, image_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{image_id}/download")


@dataclass
class RadiologyReportClient(BaseEntityClient):
    """Client for RadiologyReport entity API."""
    client: APIClient
    entity_name: str = "radiology_report"
    endpoint: str = "radiology-reports"

    def get_by_study(self, study_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/study/{study_id}")

    def sign(self, report_id: str, radiologist_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{report_id}/sign", data={"radiologist_id": radiologist_id})

    def add_findings(self, report_id: str, findings: str) -> dict:
        return self.client.put(f"{self.endpoint}/{report_id}/findings", data={"findings": findings})
