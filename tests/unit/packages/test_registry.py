"""Unit tests for Module Registry."""

from platform_core.packages import PackageStatus, RegistryEntry
from platform_core.registry import ModuleRegistry


class TestModuleRegistry:
    def test_init(self) -> None:
        registry = ModuleRegistry()
        assert registry.count() == 0

    def test_register(self) -> None:
        registry = ModuleRegistry()
        entry = RegistryEntry(name="test", version="1.0.0", publisher="test-pub")
        registry.register(entry)
        assert registry.count() == 1

    def test_get(self) -> None:
        registry = ModuleRegistry()
        entry = RegistryEntry(name="test", version="1.0.0")
        registry.register(entry)
        result = registry.get("test", "1.0.0")
        assert result is not None
        assert result.name == "test"

    def test_get_latest(self) -> None:
        registry = ModuleRegistry()
        registry.register(RegistryEntry(name="test", version="1.0.0"))
        registry.register(RegistryEntry(name="test", version="2.0.0"))
        result = registry.get("test")
        assert result is not None
        assert result.version == "2.0.0"

    def test_unregister(self) -> None:
        registry = ModuleRegistry()
        registry.register(RegistryEntry(name="test", version="1.0.0"))
        assert registry.unregister("test", "1.0.0")
        assert registry.count() == 0

    def test_unregister_nonexistent(self) -> None:
        registry = ModuleRegistry()
        assert not registry.unregister("nonexistent", "1.0.0")

    def test_list_packages(self) -> None:
        registry = ModuleRegistry()
        registry.register(RegistryEntry(name="a", version="1.0.0"))
        registry.register(RegistryEntry(name="b", version="1.0.0"))
        packages = registry.list_packages()
        assert len(packages) == 2

    def test_list_versions(self) -> None:
        registry = ModuleRegistry()
        registry.register(RegistryEntry(name="test", version="1.0.0"))
        registry.register(RegistryEntry(name="test", version="2.0.0"))
        versions = registry.list_versions("test")
        assert versions == ["1.0.0", "2.0.0"]

    def test_search(self) -> None:
        registry = ModuleRegistry()
        registry.register(RegistryEntry(name="auth-module", version="1.0.0"))
        registry.register(RegistryEntry(name="inventory", version="1.0.0"))
        results = registry.search("auth")
        assert len(results) == 1

    def test_get_latest_version(self) -> None:
        registry = ModuleRegistry()
        registry.register(RegistryEntry(name="test", version="1.0.0"))
        registry.register(RegistryEntry(name="test", version="2.0.0"))
        assert registry.get_latest_version("test") == "2.0.0"

    def test_package_exists(self) -> None:
        registry = ModuleRegistry()
        registry.register(RegistryEntry(name="test", version="1.0.0"))
        assert registry.package_exists("test", "1.0.0")
        assert not registry.package_exists("test", "2.0.0")
        assert registry.package_exists("test")

    def test_clear(self) -> None:
        registry = ModuleRegistry()
        registry.register(RegistryEntry(name="test", version="1.0.0"))
        registry.clear()
        assert registry.count() == 0

    def test_list_packages_with_status_filter(self) -> None:
        registry = ModuleRegistry()
        registry.register(RegistryEntry(name="a", version="1.0.0", status=PackageStatus.ACTIVE))
        registry.register(RegistryEntry(name="b", version="1.0.0", status=PackageStatus.DEPRECATED))
        active = registry.list_packages(status=PackageStatus.ACTIVE)
        assert len(active) == 1
        deprecated = registry.list_packages(status=PackageStatus.DEPRECATED)
        assert len(deprecated) == 1
