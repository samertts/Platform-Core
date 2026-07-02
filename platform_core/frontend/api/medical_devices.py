"""
Medical Devices API client for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class MedicalDeviceClient(BaseEntityClient):
    """Client for MedicalDevice entity API."""

    client: APIClient
    entity_name: str = "medical_device"
    endpoint: str = "medical-devices"

    def get_by_facility(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_status(self, device_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{device_id}/status")

    def connect(self, device_id: str, connection_data: dict) -> dict:
        return self.client.post(
            f"{self.endpoint}/{device_id}/connect", data=connection_data
        )

    def disconnect(self, device_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{device_id}/disconnect")


@dataclass
class DeviceConnectionClient(BaseEntityClient):
    """Client for DeviceConnection entity API."""

    client: APIClient
    entity_name: str = "device_connection"
    endpoint: str = "device-connections"

    def get_by_device(self, device_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/device/{device_id}")

    def get_active_connections(self, facility_id: str) -> dict:
        return self.client.get(
            f"{self.endpoint}/active", params={"facility_id": facility_id}
        )


@dataclass
class CalibrationClient(BaseEntityClient):
    """Client for Calibration entity API."""

    client: APIClient
    entity_name: str = "calibration"
    endpoint: str = "calibrations"

    def get_by_device(self, device_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/device/{device_id}")

    def get_due_calibrations(self, facility_id: str) -> dict:
        return self.client.get(
            f"{self.endpoint}/due", params={"facility_id": facility_id}
        )
