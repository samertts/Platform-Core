from __future__ import annotations

import pytest

from platform_core.runtime.container.engine import (
    CircularDependencyError,
    ServiceContainer,
    ServiceScope,
)


class DummyService:
    pass


class AnotherService:
    def __init__(self, dummy: DummyService) -> None:
        self.dummy = dummy


class TestServiceContainer:
    def test_register_and_resolve(self) -> None:
        container = ServiceContainer()
        container.register(DummyService)
        instance = container.resolve(DummyService)
        assert isinstance(instance, DummyService)

    def test_register_instance(self) -> None:
        container = ServiceContainer()
        dummy = DummyService()
        container.register_instance(DummyService, dummy)
        resolved = container.resolve(DummyService)
        assert resolved is dummy

    def test_singleton(self) -> None:
        container = ServiceContainer()
        container.register(DummyService, lifetime="singleton")
        i1 = container.resolve(DummyService)
        i2 = container.resolve(DummyService)
        assert i1 is i2

    def test_transient(self) -> None:
        container = ServiceContainer()
        container.register(DummyService, lifetime="transient")
        i1 = container.resolve(DummyService)
        i2 = container.resolve(DummyService)
        assert i1 is not i2

    def test_register_factory(self) -> None:
        container = ServiceContainer()
        container.register_factory(DummyService, lambda: DummyService())
        instance = container.resolve(DummyService)
        assert isinstance(instance, DummyService)

    def test_resolve_unregistered(self) -> None:
        container = ServiceContainer()
        with pytest.raises(KeyError):
            container.resolve(DummyService)

    def test_dependency_injection(self) -> None:
        container = ServiceContainer()
        container.register(DummyService)
        container.register(AnotherService)
        instance = container.resolve(AnotherService)
        assert isinstance(instance, AnotherService)
        assert isinstance(instance.dummy, DummyService)

    def test_validate_clean(self) -> None:
        container = ServiceContainer()
        container.register(DummyService)
        errors = container.validate()
        assert errors == []

    def test_create_scope(self) -> None:
        container = ServiceContainer()
        container.register(DummyService, lifetime="scoped")
        scope = container.create_scope()
        instance = scope.resolve(DummyService)
        assert isinstance(instance, DummyService)

    def test_get_registration(self) -> None:
        container = ServiceContainer()
        container.register(DummyService)
        reg = container.get_registration(DummyService)
        assert reg is not None
        assert reg["service_type"] == "DummyService"

    def test_registered_types(self) -> None:
        container = ServiceContainer()
        container.register(DummyService)
        assert "DummyService" in container.registered_types

    def test_dispose(self) -> None:
        container = ServiceContainer()
        container.register(DummyService)
        container.dispose()
