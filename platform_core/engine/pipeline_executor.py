from __future__ import annotations

from platform_core.engine.context import EngineContext
from platform_core.engine.hook_dispatcher import HookDispatcher
from platform_core.engine.result import EngineResult


class PipelineExecutor:
    """
    Executes the mandatory ENGINE_SPEC pipeline.

    Validate
        ↓
    Prepare
        ↓
    Execute
        ↓
    Finalize
    """

    def __init__(
        self,
        hooks: HookDispatcher,
    ) -> None:

        self._hooks = hooks

    def execute(
        self,
        engine,
        context: EngineContext,
    ) -> EngineResult:

        self._hooks.before_validate(engine, context)
        engine.validate(context)
        self._hooks.after_validate(engine, context)

        self._hooks.before_prepare(engine, context)
        engine.prepare(context)
        self._hooks.after_prepare(engine, context)

        self._hooks.before_execute(engine, context)

        result = engine.execute(context)

        self._hooks.after_execute(
            engine,
            context,
            result,
        )

        self._hooks.before_finalize(engine, context)
        engine.finalize(context)
        self._hooks.after_finalize(engine, context)

        return result
