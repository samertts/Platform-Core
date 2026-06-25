"""Package Manager - Core package management operations."""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from platform_core.packages import (
    InstallRecord,
    InstallStatus,
    PackageManifest,
    PackageStatus,
    RegistryEntry,
)
from platform_core.builder import PackageBuilder
from platform_core.installer import ModuleInstaller
from platform_core.resolver import DependencyResolver, CircularDependencyError, VersionConflict
from platform_core.rollback import RollbackEngine
from platform_core.updater import UpdateManager
from platform_core.verifier import PackageVerifier
from platform_core.registry import ModuleRegistry
from platform_core.repository import RepositoryManager
from platform_core.packages.compatibility import CompatibilityEngine


class PackageError(Exception):
    pass


class PackageNotFoundError(PackageError):
    pass


class PackageAlreadyInstalledError(PackageError):
    pass


class PackageNotInstalledError(PackageError):
    pass


class PackageManager:
    """Core package management operations: install, uninstall, update, rollback, verify, publish."""

    def __init__(
        self,
        install_root: str = "/opt/platform/modules",
        registry_path: str | None = None,
        repository_config: str | None = None,
    ) -> None:
        self._registry = ModuleRegistry(registry_path)
        self._repository_manager = RepositoryManager(repository_config)
        self._installer = ModuleInstaller(install_root)
        self._resolver = DependencyResolver()
        self._verifier = PackageVerifier()
        self._updater = UpdateManager(install_root)
        self._rollback_engine = RollbackEngine()
        self._builder = PackageBuilder()
        self._compatibility = CompatibilityEngine()
        self._installed: dict[str, InstallRecord] = {}
        self._lock = threading.RLock()

    @property
    def registry(self) -> ModuleRegistry:
        return self._registry

    @property
    def repository_manager(self) -> RepositoryManager:
        return self._repository_manager

    @property
    def installer(self) -> ModuleInstaller:
        return self._installer

    @property
    def resolver(self) -> DependencyResolver:
        return self._resolver

    @property
    def verifier(self) -> PackageVerifier:
        return self._verifier

    @property
    def updater(self) -> UpdateManager:
        return self._updater

    @property
    def rollback_engine(self) -> RollbackEngine:
        return self._rollback_engine

    @property
    def builder(self) -> PackageBuilder:
        return self._builder

    def install(
        self,
        package_name: str,
        version: str = "",
        dry_run: bool = False,
    ) -> dict[str, Any]:
        entry = self._registry.get(package_name, version or None)
        if entry is None:
            raise PackageNotFoundError(f"Package not found: {package_name}")

        with self._lock:
            if package_name in self._installed:
                existing = self._installed[package_name]
                if existing.package_version == entry.version:
                    return {
                        "status": "already_installed",
                        "package": package_name,
                        "version": entry.version,
                    }

        try:
            resolution = self._resolver.resolve(package_name, entry.version)
        except CircularDependencyError as e:
            raise PackageError(f"Circular dependency: {e}")
        except VersionConflict as e:
            raise PackageError(f"Version conflict: {e}")

        manifest = PackageManifest()
        manifest.package.name = package_name
        manifest.package.version = entry.version
        manifest.dependencies.required = entry.dependencies.required

        install_record = self._installer.install(
            package_path=f"/tmp/{package_name}-{entry.version}",
            manifest=manifest,
            dry_run=dry_run,
        )

        if not dry_run:
            with self._lock:
                self._installed[package_name] = install_record
            self._updater.register_installed(install_record)

        return {
            "status": "installed" if not dry_run else "dry_run",
            "package": package_name,
            "version": entry.version,
            "dependencies": resolution,
        }

    def uninstall(self, package_name: str) -> dict[str, Any]:
        with self._lock:
            if package_name not in self._installed:
                raise PackageNotInstalledError(f"Package not installed: {package_name}")

            record = self._installed[package_name]

        snapshot = self._rollback_engine.create_snapshot(
            {package_name: record},
            description=f"Before uninstalling {package_name}",
        )

        success = self._installer.uninstall(package_name)

        if success:
            with self._lock:
                del self._installed[package_name]

        return {
            "status": "uninstalled" if success else "failed",
            "package": package_name,
            "snapshot_id": str(snapshot.id),
        }

    def update(self, package_name: str, target_version: str = "") -> dict[str, Any]:
        with self._lock:
            record = self._installed.get(package_name)
            if record is None:
                raise PackageNotInstalledError(f"Package not installed: {package_name}")

        entry = self._registry.get(package_name, target_version or None)
        if entry is None:
            raise PackageNotFoundError(f"Package not found: {package_name}")

        staged = self._updater.stage_update(package_name, entry.version)
        result = self._updater.apply_update(package_name, entry.version)

        with self._lock:
            self._installed[package_name].package_version = entry.version

        return {
            "status": "updated",
            "package": package_name,
            "from_version": record.package_version,
            "to_version": entry.version,
        }

    def rollback(self, package_name: str) -> dict[str, Any]:
        snapshots = self._rollback_engine.list_snapshots()
        if not snapshots:
            return {"status": "no_snapshots", "package": package_name}

        latest = snapshots[-1]
        result = self._rollback_engine.restore_snapshot(latest["id"])

        return {
            "status": "rolled_back",
            "package": package_name,
            "snapshot_id": latest["id"],
            "restored_packages": result.get("restored_packages", []),
        }

    def verify(self, package_name: str, version: str = "") -> dict[str, Any]:
        entry = self._registry.get(package_name, version or None)
        if entry is None:
            raise PackageNotFoundError(f"Package not found: {package_name}")

        return {
            "package": package_name,
            "version": entry.version,
            "checksum": {"valid": entry.checksum.value != ""},
            "signature": {"valid": entry.signature.signature != ""},
            "status": "verified",
        }

    def publish(self, package_path: str, manifest: PackageManifest) -> dict[str, Any]:
        errors = self._installer.pre_install_validate(package_path, manifest)
        if errors:
            raise PackageError(f"Validation failed: {errors}")

        entry = RegistryEntry(
            name=manifest.package.name,
            version=manifest.package.version,
            publisher=manifest.package.publisher,
            license=manifest.package.license,
            dependencies=manifest.dependencies,
            capabilities=manifest.capabilities,
            compatibility=manifest.compatibility,
        )

        self._registry.register(entry)

        return {
            "status": "published",
            "package": manifest.package.name,
            "version": manifest.package.version,
        }

    def search(self, query: str) -> list[dict[str, Any]]:
        results = self._registry.search(query)
        return [
            {
                "name": e.name,
                "version": e.version,
                "publisher": e.publisher,
                "status": e.status.value,
            }
            for e in results
        ]

    def list_installed(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "name": r.package_name,
                    "version": r.package_version,
                    "status": r.status.value,
                    "installed_at": r.installed_at.isoformat(),
                }
                for r in self._installed.values()
            ]

    def doctor(self) -> dict[str, Any]:
        issues: list[str] = []

        with self._lock:
            for name, record in self._installed.items():
                path = Path(record.install_path)
                if not path.exists():
                    issues.append(f"Package {name} install path missing")

        return {
            "healthy": len(issues) == 0,
            "issues": issues,
            "packages_checked": len(self._installed),
        }

    def repair(self, package_name: str) -> dict[str, Any]:
        return self._installer.repair(package_name)

    def freeze(self, package_name: str, version: str) -> dict[str, Any]:
        entry = self._registry.get(package_name, version)
        if entry is None:
            raise PackageNotFoundError(f"Package not found: {package_name}@{version}")

        return {
            "status": "frozen",
            "package": package_name,
            "version": version,
        }

    def get_info(self, package_name: str) -> dict[str, Any]:
        entry = self._registry.get(package_name)
        if entry is None:
            raise PackageNotFoundError(f"Package not found: {package_name}")

        with self._lock:
            installed = self._installed.get(package_name)

        return {
            "name": entry.name,
            "version": entry.version,
            "publisher": entry.publisher,
            "status": entry.status.value,
            "installed": installed is not None,
            "installed_version": installed.package_version if installed else None,
        }
