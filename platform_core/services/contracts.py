from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IServiceFactory(ABC):
    @abstractmethod
    def create(self) -> Any:
        raise NotImplementedError


class IServiceProvider(ABC):
    @abstractmethod
    def create(
        self,
        descriptor: Any,
        scope: Any | None = None,
    ) -> Any:
        raise NotImplementedError


class IServiceRegistry(ABC):
    @abstractmethod
    def register(
        self,
        descriptor: Any,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        key: str,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        key: str,
    ) -> bool:
        raise NotImplementedError
