from inspect import isabstract

from platform_core.engine.abc import Engine


def test_engine_is_abstract() -> None:

    assert isabstract(Engine)


def test_engine_has_run() -> None:

    assert hasattr(Engine, "run")


def test_engine_has_validate() -> None:

    assert hasattr(Engine, "validate")


def test_engine_has_prepare() -> None:

    assert hasattr(Engine, "prepare")


def test_engine_has_execute() -> None:

    assert hasattr(Engine, "execute")


def test_engine_has_finalize() -> None:

    assert hasattr(Engine, "finalize")
