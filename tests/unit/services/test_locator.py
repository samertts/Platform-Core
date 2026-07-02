from platform_core.services.collection import ServiceCollection
from platform_core.services.container import ServiceContainer
from platform_core.services.locator import ServiceLocator


class Logger:
    pass


def test_locator():

    container = ServiceContainer()

    services = ServiceCollection()

    services.add_singleton(
        "logger",
        Logger,
    )

    for descriptor in services.descriptors:
        container.register(descriptor)

    locator = ServiceLocator(container)

    assert locator.exists("logger")

    instance = locator.resolve("logger")

    assert isinstance(instance, Logger)
