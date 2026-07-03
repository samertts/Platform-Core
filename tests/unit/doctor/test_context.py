from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from platform_core.doctor.context import DoctorContext


def test_context_defaults() -> None:

    context = DoctorContext(
        project_root=Path("."),
    )

    assert context.strict is False
    assert context.fix is False
    assert context.include == ()
    assert context.exclude == ()


def test_context_immutable() -> None:

    context = DoctorContext(
        project_root=Path("."),
    )

    with pytest.raises(FrozenInstanceError):
        setattr(context, "strict", True)
