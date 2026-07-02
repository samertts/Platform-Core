"""
Epidemiology domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field

from .base import BaseEntity


@dataclass
class Disease(BaseEntity):
    """Disease record."""

    name: str = ""
    icd_code: str | None = None
    snomed_code: str | None = None
    category: str = ""
    transmission_mode: str | None = None
    incubation_period: str | None = None
    severity: str = "moderate"
    is_notifiable: bool = False


@dataclass
class Outbreak(BaseEntity):
    """Disease outbreak record."""

    disease_id: str = ""
    outbreak_name: str = ""
    start_date: str = ""
    end_date: str | None = None
    location: str = ""
    cases_count: int = 0
    deaths_count: int = 0
    status: str = "active"
    response_team: list[str] = field(default_factory=list)
