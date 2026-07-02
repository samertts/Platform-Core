from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from platform_core.doctor.check_result import CheckResult


class DoctorCheck(ABC):
    """
    Base class for every Doctor check.
    """

    id: str

    name: str

    @abstractmethod
    def run(self) -> CheckResult:
        """
        Execute the check.
        """
