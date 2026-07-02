from __future__ import annotations

import inspect
from typing import Any

from platform_core.services.descriptor import ServiceDescriptor


class ObjectActivator:
    """
    Responsible only for constructing object instances.
    """

    def create(
        self,
        descriptor: ServiceDescriptor,
    ) -> Any:

        implementation = descriptor.implementation

        signature = inspect.signature(
            implementation.__init__,
        )

        parameters = []

        for parameter in list(signature.parameters.values())[1:]:
            #
            # Ignore object.__init__(*args, **kwargs)
            #

            if parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue

            parameters.append(parameter)

        if parameters:
            raise NotImplementedError("Constructor Injection is not implemented yet.")

        return implementation()
