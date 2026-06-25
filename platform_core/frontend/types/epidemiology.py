"""
Epidemiology domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional
from .base import BaseEntity


@dataclass
class Disease(BaseEntity):
    """Disease record."""
    name: str = ""
    icd_code: Optional[str] = None
    snomed_code: Optional[str] = None
    category: str = ""
    transmission_mode: Optional[str] = None
    incubation_period: Optional[str] = None
    severity: str = "moderate"
    is_notifiable: bool = False


@dataclass
class Outbreak(BaseEntity):
    """Disease outbreak record."""
    disease_id: str = ""
    outbreak_name: str = ""
    start_date: str = ""
    end_date: Optional[str] = None
    location: str = ""
    cases_count: int = 0
    deaths_count: int = 0
    status: str = "active"
    response_team: list[str] = field(default_factory=list)
