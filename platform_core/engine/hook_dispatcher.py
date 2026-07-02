from __future__ import annotations

from platform_core.engine.context import EngineContext
from platform_core.engine.result import EngineResult


class HookDispatcher:
    """
    Responsible for invoking all Engine hooks.

    BaseEngine should never call hooks directly.
    """

    def before_validate(
        self,
        engine,
        context: EngineContext,
    ) -> None:
        engine.before_validate(context)

    def after_validate(
        self,
        engine,
        context: EngineContext,
    ) -> None:
        engine.after_validate(context)

    def before_prepare(
        self,
        engine,
        context: EngineContext,
    ) -> None:
        engine.before_prepare(context)

    def after_prepare(
        self,
        engine,
        context: EngineContext,
    ) -> None:
        engine.after_prepare(context)

    def before_execute(
        self,
        engine,
        context: EngineContext,
    ) -> None:
        engine.before_execute(context)

    def after_execute(
        self,
        engine,
        context: EngineContext,
        result: EngineResult,
    ) -> None:
        engine.after_execute(context, result)

    def before_finalize(
        self,
        engine,
        context: EngineContext,
    ) -> None:
        engine.before_finalize(context)

    def after_finalize(
        self,
        engine,
        context: EngineContext,
    ) -> None:
        engine.after_finalize(context)

    def on_failure(
        self,
        engine,
        context: EngineContext,
        exc: Exception,
    ) -> None:
        engine.on_failure(context, exc)
