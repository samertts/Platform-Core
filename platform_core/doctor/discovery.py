from __future__ import annotations

import importlib
import inspect
import pkgutil

import platform_core.doctor.checks as checks_package

from platform_core.doctor.check import DoctorCheck


def discover_checks() -> list[DoctorCheck]:

    checks: list[DoctorCheck] = []

    for module in pkgutil.iter_modules(checks_package.__path__):

        mod = importlib.import_module(
            f"{checks_package.__name__}.{module.name}"
        )

        for _, obj in inspect.getmembers(mod, inspect.isclass):

            if (
                issubclass(obj, DoctorCheck)
                and obj is not DoctorCheck
            ):
                checks.append(obj())

    checks.sort(key=lambda c: c.name)

    return checks
