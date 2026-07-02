from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from platform_core.doctor.context import DoctorContext


def test_context_defaults():

    context = DoctorContext(
        project_root=Path("."),
    )

    assert context.strict is False
    assert context.fix is False
    assert context.include == ()
    assert context.exclude == ()


def test_context_immutable():

    context = DoctorContext(
        project_root=Path("."),
    )

    with pytest.raises(FrozenInstanceError):
        context.strict = True
