"""
Medical Devices domain types for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntity


@dataclass
class MedicalDevice(BaseEntity):
    """Medical device record."""

    facility_id: str = ""
    department_id: str | None = None
    device_type: str = ""
    manufacturer: str = ""
    model: str = ""
    serial_number: str = ""
    location: str | None = None
    status: str = "active"
    last_maintenance_date: str | None = None
    next_maintenance_date: str | None = None


@dataclass
class DeviceConnection(BaseEntity):
    """Device connection record."""

    device_id: str = ""
    connection_type: str = ""
    connection_string: str | None = None
    protocol: str | None = None
    status: str = "connected"
    connected_at: str | None = None
    disconnected_at: str | None = None


@dataclass
class Calibration(BaseEntity):
    """Device calibration record."""

    device_id: str = ""
    calibration_type: str = ""
    calibration_date: str = ""
    next_calibration_date: str | None = None
    performed_by: str | None = None
    result: str = "pass"
    notes: str | None = None
