from __future__ import annotations

from platform_core.services.collection import ServiceCollection
from platform_core.services.container import ServiceContainer


class ContainerBuilder:
    """
    Builds a ServiceContainer from a ServiceCollection.
    """

    def build(
        self,
        services: ServiceCollection,
    ) -> ServiceContainer:

        container = ServiceContainer()

        for descriptor in services.descriptors:
            container.register(
                descriptor,
            )

        return container
