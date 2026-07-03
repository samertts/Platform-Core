"""
Medical Devices API client for NHDOS Frontend
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class MedicalDeviceClient(BaseEntityClient[Any]):
    """Client for MedicalDevice entity API."""

    client: APIClient
    entity_name: str = "medical_device"
    endpoint: str = "medical-devices"

    def get_by_facility(self, facility_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_status(self, device_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/{device_id}/status")

    def connect(self, device_id: str, connection_data: dict[str, Any]) -> dict[str, Any]:
        return self.client.post(f"{self.endpoint}/{device_id}/connect", data=connection_data)

    def disconnect(self, device_id: str) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{device_id}/disconnect")


@dataclass
class DeviceConnectionClient(BaseEntityClient[Any]):
    """Client for DeviceConnection entity API."""

    client: APIClient
    entity_name: str = "device_connection"
    endpoint: str = "device-connections"

    def get_by_device(self, device_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/device/{device_id}")

    def get_active_connections(self, facility_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/active", params={"facility_id": facility_id})


@dataclass
class CalibrationClient(BaseEntityClient[Any]):
    """Client for Calibration entity API."""

    client: APIClient
    entity_name: str = "calibration"
    endpoint: str = "calibrations"

    def get_by_device(self, device_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/device/{device_id}")

    def get_due_calibrations(self, facility_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/due", params={"facility_id": facility_id})
