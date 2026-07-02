from __future__ import annotations

from abc import ABC, abstractmethod

from platform_core.engine.context import EngineContext
from platform_core.engine.result import EngineResult


class Engine(ABC):
    """
    Abstract Engine contract.

    Every Engine implementation inside Platform-Core MUST implement
    this interface.
    """

    @abstractmethod
    def run(
        self,
        context: EngineContext,
    ) -> EngineResult:
        """
        Execute the complete Engine lifecycle.
        """
        raise NotImplementedError

    @abstractmethod
    def validate(
        self,
        context: EngineContext,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def prepare(
        self,
        context: EngineContext,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        context: EngineContext,
    ) -> EngineResult:
        raise NotImplementedError

    @abstractmethod
    def finalize(
        self,
        context: EngineContext,
    ) -> None:
        raise NotImplementedError

    # ---------- Hooks ----------

    def before_validate(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def after_validate(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def before_prepare(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def after_prepare(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def before_execute(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def after_execute(
        self,
        context: EngineContext,
        result: EngineResult,
    ) -> None:
        pass

    def before_finalize(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def after_finalize(
        self,
        context: EngineContext,
    ) -> None:
        pass

    def on_failure(
        self,
        context: EngineContext,
        error: Exception,
    ) -> None:
        pass
