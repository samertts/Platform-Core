from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class IServiceContainer(ABC):

    @abstractmethod
    def register_singleton(
        self,
        interface: type,
        implementation: type,
    ) -> None:
        ...

    @abstractmethod
    def register_transient(
        self,
        interface: type,
        implementation: type,
    ) -> None:
        ...

    @abstractmethod
    def resolve(
        self,
        interface: type,
    ) -> Any:
        ...
