import pytest

from platform_core.services.activator import ObjectActivator
from platform_core.services.descriptor import ServiceDescriptor


class Logger:
    pass


class Repository:
    def __init__(
        self,
        logger: Logger,
    ) -> None:

        self.logger = logger


def test_create():

    descriptor = ServiceDescriptor(
        key="logger",
        implementation=Logger,
    )

    instance = ObjectActivator().create(
        descriptor,
    )

    assert isinstance(
        instance,
        Logger,
    )


def test_constructor_not_supported():

    descriptor = ServiceDescriptor(
        key="repository",
        implementation=Repository,
    )

    with pytest.raises(
        NotImplementedError,
    ):
        ObjectActivator().create(
            descriptor,
        )
