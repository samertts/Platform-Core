"""Package SDK - Python SDK, CLI SDK, Runtime SDK, Publishing SDK."""

from __future__ import annotations

from typing import Any

from platform_core.packages import (PackageManifest, RegistryEntry,
                                    RepositoryConfig)
from platform_core.packages.manager import PackageManager


class PlatformSDK:
    """Python SDK for the Platform Package Manager."""

    def __init__(
        self,
        install_root: str = "/opt/platform/modules",
        registry_path: str | None = None,
    ) -> None:
        self._manager = PackageManager(
            install_root=install_root,
            registry_path=registry_path,
        )

    @property
    def manager(self) -> PackageManager:
        return self._manager

    def install(self, package: str, version: str = "") -> dict[str, Any]:
        return self._manager.install(package, version)

    def uninstall(self, package: str) -> dict[str, Any]:
        return self._manager.uninstall(package)

    def update(self, package: str, version: str = "") -> dict[str, Any]:
        return self._manager.update(package, version)

    def search(self, query: str) -> list[dict[str, Any]]:
        return self._manager.search(query)

    def list_installed(self) -> list[dict[str, Any]]:
        return self._manager.list_installed()

    def verify(self, package: str) -> dict[str, Any]:
        return self._manager.verify(package)

    def doctor(self) -> dict[str, Any]:
        return self._manager.doctor()

    def rollback(self, package: str) -> dict[str, Any]:
        return self._manager.rollback(package)

    def repair(self, package: str) -> dict[str, Any]:
        return self._manager.repair(package)

    def get_info(self, package: str) -> dict[str, Any]:
        return self._manager.get_info(package)

    def publish(
        self,
        path: str,
        name: str,
        version: str,
        publisher: str = "",
        dependencies: list[dict[str, Any]] | None = None,
        capabilities: dict[str, list[str]] | None = None,
    ) -> dict[str, Any]:
        manifest = PackageManifest()
        manifest.package.name = name
        manifest.package.version = version
        manifest.package.publisher = publisher
        if dependencies:
            manifest.dependencies.required = dependencies
        if capabilities:
            manifest.capabilities.provides = capabilities.get("provides", [])
            manifest.capabilities.requires = capabilities.get("requires", [])
        return self._manager.publish(path, manifest)

    def add_repository(
        self,
        name: str,
        url: str = "",
        repo_type: str = "local",
        priority: int = 0,
    ) -> None:
        from platform_core.packages import RepositoryType

        config = RepositoryConfig(
            name=name,
            type=RepositoryType(repo_type),
            url=url,
            priority=priority,
        )
        self._manager.repository_manager.add_repository(config)

    def remove_repository(self, name: str) -> bool:
        return self._manager.repository_manager.remove_repository(name)

    def list_repositories(self) -> list[dict[str, Any]]:
        repos = self._manager.repository_manager.list_repositories()
        return [
            {"name": r.name, "type": r.type.value, "url": r.url, "enabled": r.enabled}
            for r in repos
        ]


class PublishingSDK:
    """SDK for publishing packages to the Platform registry."""

    def __init__(self, sdk: PlatformSDK | None = None) -> None:
        self._sdk = sdk or PlatformSDK()

    def build_and_publish(
        self,
        source_dir: str,
        name: str,
        version: str,
        publisher: str = "",
        private_key: str = "",
    ) -> dict[str, Any]:
        manifest = self._sdk.manager.builder.generate_manifest(
            name=name,
            version=version,
            publisher=publisher,
        )

        package_path = self._sdk.manager.builder.build_package(
            source_dir=source_dir,
            manifest=manifest,
            sign=bool(private_key),
            private_key=private_key,
        )

        result = self._sdk.publish(
            path=package_path,
            name=name,
            version=version,
            publisher=publisher,
        )

        return {
            "package_path": package_path,
            "publish_result": result,
        }


class RuntimeSDK:
    """SDK for runtime integration with the package manager."""

    def __init__(self, sdk: PlatformSDK | None = None) -> None:
        self._sdk = sdk or PlatformSDK()
        self._loaded_modules: dict[str, Any] = {}

    def load_module(self, package_name: str) -> Any:
        if package_name in self._loaded_modules:
            return self._loaded_modules[package_name]

        info = self._sdk.get_info(package_name)
        if not info.get("installed"):
            raise ImportError(f"Package not installed: {package_name}")

        self._loaded_modules[package_name] = info
        return info

    def unload_module(self, package_name: str) -> None:
        self._loaded_modules.pop(package_name, None)

    def list_loaded(self) -> list[str]:
        return list(self._loaded_modules.keys())

    def verify_loaded(self) -> dict[str, Any]:
        results: dict[str, Any] = {}
        for name in self._loaded_modules:
            try:
                verification = self._sdk.verify(name)
                results[name] = verification.get("status") == "verified"
            except Exception:
                results[name] = False
        return results
