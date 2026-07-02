import pytest

from platform_core.workflow.pipeline import WorkflowPipeline
from platform_core.workflow.validator import WorkflowValidator


def test_empty_pipeline():

    validator = WorkflowValidator()

    with pytest.raises(ValueError):

        validator.validate(
            WorkflowPipeline(),
        )
