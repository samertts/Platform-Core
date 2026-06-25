from __future__ import annotations

import pytest

from platform_core.runtime.identity.engine import IdentityEngine


class TestIdentityEngine:
    def test_runtime_identity(self) -> None:
        engine = IdentityEngine(runtime_name="test", runtime_version="1.0.0")
        identity = engine.runtime_identity
        assert identity.name == "test"
        assert identity.version == "1.0.0"
        assert identity.type == "runtime"

    def test_get_module_identity(self) -> None:
        engine = IdentityEngine()
        identity = engine.get_module_identity("test-module")
        assert identity.name == "test-module"
        assert identity.type == "module"

    def test_get_module_identity_cached(self) -> None:
        engine = IdentityEngine()
        id1 = engine.get_module_identity("test")
        id2 = engine.get_module_identity("test")
        assert id1.id == id2.id

    def test_get_service_identity(self) -> None:
        engine = IdentityEngine()
        identity = engine.get_service_identity("test-service")
        assert identity.name == "test-service"
        assert identity.type == "service"

    def test_register_module(self) -> None:
        engine = IdentityEngine()
        identity = engine.register_module("mod", "2.0.0")
        assert identity.name == "mod"
        assert identity.version == "2.0.0"

    def test_register_service(self) -> None:
        engine = IdentityEngine()
        identity = engine.register_service("svc", "3.0.0")
        assert identity.name == "svc"
        assert identity.version == "3.0.0"

    def test_list_modules(self) -> None:
        engine = IdentityEngine()
        engine.register_module("a", "1.0.0")
        engine.register_module("b", "2.0.0")
        modules = engine.list_modules()
        assert len(modules) == 2
        names = {m["name"] for m in modules}
        assert "a" in names
        assert "b" in names

    def test_list_services(self) -> None:
        engine = IdentityEngine()
        engine.register_service("x", "1.0.0")
        services = engine.list_services()
        assert len(services) == 1

    def test_load_certificate_not_found(self) -> None:
        engine = IdentityEngine()
        with pytest.raises(FileNotFoundError):
            engine.load_certificate("/nonexistent/cert.pem")

    def test_verify_signature(self) -> None:
        engine = IdentityEngine()
        assert engine.verify_signature(b"test", b"sig") is True
        assert engine.verify_signature(b"test", b"") is False
