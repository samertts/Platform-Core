from inspect import isabstract

from platform_core.engine.abc import Engine


def test_engine_is_abstract():

    assert isabstract(Engine)


def test_engine_has_run():

    assert hasattr(Engine, "run")


def test_engine_has_validate():

    assert hasattr(Engine, "validate")


def test_engine_has_prepare():

    assert hasattr(Engine, "prepare")


def test_engine_has_execute():

    assert hasattr(Engine, "execute")


def test_engine_has_finalize():

    assert hasattr(Engine, "finalize")
