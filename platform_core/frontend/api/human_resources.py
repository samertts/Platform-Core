"""
Human Resources API client for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class ProfessionalClient(BaseEntityClient):
    """Client for Professional entity API."""

    client: APIClient
    entity_name: str = "professional"
    endpoint: str = "professionals"

    def get_by_citizen(self, citizen_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/citizen/{citizen_id}")

    def get_by_facility(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_by_specialty(self, specialty: str) -> dict:
        return self.client.get(f"{self.endpoint}/specialty/{specialty}")


@dataclass
class LicenseClient(BaseEntityClient):
    """Client for License entity API."""

    client: APIClient
    entity_name: str = "license"
    endpoint: str = "licenses"

    def get_by_professional(self, professional_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/professional/{professional_id}")

    def verify(self, license_number: str) -> dict:
        return self.client.get(f"{self.endpoint}/verify/{license_number}")

    def suspend(self, license_id: str, reason: str) -> dict:
        return self.client.put(f"{self.endpoint}/{license_id}/suspend", data={"reason": reason})

    def reinstate(self, license_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{license_id}/reinstate")


@dataclass
class OrganizationClient(BaseEntityClient):
    """Client for Organization entity API."""

    client: APIClient
    entity_name: str = "organization"
    endpoint: str = "organizations"

    def get_by_type(self, organization_type: str) -> dict:
        return self.client.get(f"{self.endpoint}/type/{organization_type}")

    def get_facilities(self, organization_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{organization_id}/facilities")


@dataclass
class FacilityClient(BaseEntityClient):
    """Client for Facility entity API."""

    client: APIClient
    entity_name: str = "facility"
    endpoint: str = "facilities"

    def get_by_organization(self, organization_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/organization/{organization_id}")

    def get_by_type(self, facility_type: str) -> dict:
        return self.client.get(f"{self.endpoint}/type/{facility_type}")

    def get_departments(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{facility_id}/departments")

    def get_beds(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{facility_id}/beds")

    def get_capacity(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{facility_id}/capacity")


@dataclass
class DepartmentClient(BaseEntityClient):
    """Client for Department entity API."""

    client: APIClient
    entity_name: str = "department"
    endpoint: str = "departments"

    def get_by_facility(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_rooms(self, department_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{department_id}/rooms")


@dataclass
class RoomClient(BaseEntityClient):
    """Client for Room entity API."""

    client: APIClient
    entity_name: str = "room"
    endpoint: str = "rooms"

    def get_by_department(self, department_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/department/{department_id}")

    def get_available(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/available", params={"facility_id": facility_id})

    def get_beds(self, room_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{room_id}/beds")


@dataclass
class BedClient(BaseEntityClient):
    """Client for Bed entity API."""

    client: APIClient
    entity_name: str = "bed"
    endpoint: str = "beds"

    def get_by_room(self, room_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/room/{room_id}")

    def get_available(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/available", params={"facility_id": facility_id})

    def assign(self, bed_id: str, patient_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{bed_id}/assign", data={"patient_id": patient_id})

    def release(self, bed_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/{bed_id}/release")


@dataclass
class EmployeeClient(BaseEntityClient):
    """Client for Employee entity API."""

    client: APIClient
    entity_name: str = "employee"
    endpoint: str = "employees"

    def get_by_organization(self, organization_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/organization/{organization_id}")

    def get_by_department(self, department_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/department/{department_id}")


@dataclass
class AttendanceClient(BaseEntityClient):
    """Client for Attendance entity API."""

    client: APIClient
    entity_name: str = "attendance"
    endpoint: str = "attendance"

    def get_by_employee(self, employee_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/employee/{employee_id}")

    def clock_in(self, employee_id: str) -> dict:
        return self.client.post(f"{self.endpoint}/clock-in", data={"employee_id": employee_id})

    def clock_out(self, employee_id: str) -> dict:
        return self.client.put(f"{self.endpoint}/clock-out", data={"employee_id": employee_id})


@dataclass
class LeaveClient(BaseEntityClient):
    """Client for Leave entity API."""

    client: APIClient
    entity_name: str = "leave"
    endpoint: str = "leaves"

    def get_by_employee(self, employee_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/employee/{employee_id}")

    def approve(self, leave_id: str, approver_id: str) -> dict:
        return self.client.put(
            f"{self.endpoint}/{leave_id}/approve", data={"approver_id": approver_id}
        )

    def reject(self, leave_id: str, reason: str) -> dict:
        return self.client.put(f"{self.endpoint}/{leave_id}/reject", data={"reason": reason})
