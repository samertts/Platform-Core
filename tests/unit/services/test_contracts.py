from inspect import isabstract

from platform_core.services.contracts import IServiceFactory, IServiceProvider, IServiceRegistry


def test_factory_is_abstract() -> None:

    assert isabstract(IServiceFactory)


def test_provider_is_abstract() -> None:

    assert isabstract(IServiceProvider)


def test_registry_is_abstract() -> None:

    assert isabstract(IServiceRegistry)
