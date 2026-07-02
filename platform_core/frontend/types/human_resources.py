"""
Human Resources domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class Professional(BaseEntity):
    """Healthcare professional record."""

    citizen_id: str = ""
    professional_type: str = ""
    specialty: Optional[str] = None
    license_number: Optional[str] = None
    facility_id: Optional[str] = None
    department_id: Optional[str] = None
    status: str = "active"


@dataclass
class License(BaseEntity):
    """Professional license record."""

    professional_id: str = ""
    license_type: str = ""
    license_number: str = ""
    issuing_authority: str = ""
    issue_date: str = ""
    expiry_date: str = ""
    status: str = "active"
    restrictions: list[str] = field(default_factory=list)


@dataclass
class Organization(BaseEntity):
    """Healthcare organization record."""

    name: str = ""
    organization_type: str = ""
    parent_organization_id: Optional[str] = None
    registration_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: str = "active"


@dataclass
class Facility(BaseEntity):
    """Healthcare facility record."""

    organization_id: str = ""
    name: str = ""
    facility_type: str = ""
    facility_code: str = ""
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    capacity: Optional[int] = None
    status: str = "active"


@dataclass
class Department(BaseEntity):
    """Facility department record."""

    facility_id: str = ""
    name: str = ""
    department_code: str = ""
    department_type: str = ""
    head_of_department_id: Optional[str] = None
    phone: Optional[str] = None
    status: str = "active"


@dataclass
class Room(BaseEntity):
    """Department room record."""

    department_id: str = ""
    room_number: str = ""
    room_type: str = ""
    capacity: int = 1
    status: str = "available"


@dataclass
class Bed(BaseEntity):
    """Room bed record."""

    room_id: str = ""
    bed_number: str = ""
    bed_type: str = ""
    status: str = "available"
    patient_id: Optional[str] = None


@dataclass
class Employee(BaseEntity):
    """Organization employee record."""

    organization_id: str = ""
    citizen_id: str = ""
    employee_number: str = ""
    position: str = ""
    department_id: Optional[str] = None
    hire_date: str = ""
    employment_type: str = "full_time"
    status: str = "active"


@dataclass
class Attendance(BaseEntity):
    """Employee attendance record."""

    employee_id: str = ""
    date: str = ""
    clock_in: Optional[str] = None
    clock_out: Optional[str] = None
    hours_worked: Optional[float] = None
    status: str = "present"


@dataclass
class Leave(BaseEntity):
    """Employee leave record."""

    employee_id: str = ""
    leave_type: str = ""
    start_date: str = ""
    end_date: str = ""
    reason: Optional[str] = None
    status: str = "pending"
    approved_by: Optional[str] = None
