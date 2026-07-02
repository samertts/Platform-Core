from __future__ import annotations

from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    Base plugin contract.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError
