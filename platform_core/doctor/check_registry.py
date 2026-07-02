from __future__ import annotations

from collections.abc import Iterable

from platform_core.doctor.check import DoctorCheck


class CheckRegistry:
    """
    Stores and exposes Doctor checks.
    """

    def __init__(self) -> None:
        self._checks: dict[str, DoctorCheck] = {}

    def register(
        self,
        check: DoctorCheck,
    ) -> None:

        if check.id in self._checks:
            raise ValueError(
                f"Duplicate check id: {check.id}"
            )

        self._checks[check.id] = check

    def unregister(
        self,
        check_id: str,
    ) -> None:

        self._checks.pop(check_id, None)

    def get(
        self,
        check_id: str,
    ) -> DoctorCheck:

        return self._checks[check_id]

    def exists(
        self,
        check_id: str,
    ) -> bool:

        return check_id in self._checks

    def clear(self) -> None:

        self._checks.clear()

    def all(self) -> tuple[DoctorCheck, ...]:

        return tuple(self._checks.values())

    def ids(self) -> tuple[str, ...]:

        return tuple(self._checks.keys())

    def __len__(self) -> int:

        return len(self._checks)

    def __iter__(self) -> Iterable[DoctorCheck]:

        return iter(self._checks.values())
