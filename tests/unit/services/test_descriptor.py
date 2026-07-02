from dataclasses import FrozenInstanceError

import pytest

from platform_core.services.descriptor import ServiceDescriptor
from platform_core.services.lifetime import ServiceLifetime


class Service:
    pass


def test_descriptor():

    descriptor = ServiceDescriptor(
        key="service",
        implementation=Service,
    )

    assert descriptor.key == "service"

    assert descriptor.implementation is Service

    assert descriptor.lifetime is ServiceLifetime.SINGLETON


def test_descriptor_immutable():

    descriptor = ServiceDescriptor(
        key="service",
        implementation=Service,
    )

    with pytest.raises(FrozenInstanceError):
        descriptor.key = "other"
