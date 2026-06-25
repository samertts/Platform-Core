"""
Medical Devices domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional
from .base import BaseEntity


@dataclass
class MedicalDevice(BaseEntity):
    """Medical device record."""
    facility_id: str = ""
    department_id: Optional[str] = None
    device_type: str = ""
    manufacturer: str = ""
    model: str = ""
    serial_number: str = ""
    location: Optional[str] = None
    status: str = "active"
    last_maintenance_date: Optional[str] = None
    next_maintenance_date: Optional[str] = None


@dataclass
class DeviceConnection(BaseEntity):
    """Device connection record."""
    device_id: str = ""
    connection_type: str = ""
    connection_string: Optional[str] = None
    protocol: Optional[str] = None
    status: str = "connected"
    connected_at: Optional[str] = None
    disconnected_at: Optional[str] = None


@dataclass
class Calibration(BaseEntity):
    """Device calibration record."""
    device_id: str = ""
    calibration_type: str = ""
    calibration_date: str = ""
    next_calibration_date: Optional[str] = None
    performed_by: Optional[str] = None
    result: str = "pass"
    notes: Optional[str] = None
