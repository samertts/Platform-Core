"""
Human Resources domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field

from .base import BaseEntity


@dataclass
class Professional(BaseEntity):
    """Healthcare professional record."""

    citizen_id: str = ""
    professional_type: str = ""
    specialty: str | None = None
    license_number: str | None = None
    facility_id: str | None = None
    department_id: str | None = None
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
    parent_organization_id: str | None = None
    registration_number: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    status: str = "active"


@dataclass
class Facility(BaseEntity):
    """Healthcare facility record."""

    organization_id: str = ""
    name: str = ""
    facility_type: str = ""
    facility_code: str = ""
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    capacity: int | None = None
    status: str = "active"


@dataclass
class Department(BaseEntity):
    """Facility department record."""

    facility_id: str = ""
    name: str = ""
    department_code: str = ""
    department_type: str = ""
    head_of_department_id: str | None = None
    phone: str | None = None
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
    patient_id: str | None = None


@dataclass
class Employee(BaseEntity):
    """Organization employee record."""

    organization_id: str = ""
    citizen_id: str = ""
    employee_number: str = ""
    position: str = ""
    department_id: str | None = None
    hire_date: str = ""
    employment_type: str = "full_time"
    status: str = "active"


@dataclass
class Attendance(BaseEntity):
    """Employee attendance record."""

    employee_id: str = ""
    date: str = ""
    clock_in: str | None = None
    clock_out: str | None = None
    hours_worked: float | None = None
    status: str = "present"


@dataclass
class Leave(BaseEntity):
    """Employee leave record."""

    employee_id: str = ""
    leave_type: str = ""
    start_date: str = ""
    end_date: str = ""
    reason: str | None = None
    status: str = "pending"
    approved_by: str | None = None
