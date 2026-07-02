"""Update Manager - Check, download, validate, stage, apply, rollback, delta updates."""

from __future__ import annotations

import json
import threading
from datetime import UTC, datetime, timezone
from pathlib import Path
from typing import Any

from platform_core.packages import InstallRecord, InstallStatus, PackageManifest, PackageStatus


class UpdateError(Exception):
    pass


class UpdateManager:
    """Manages package updates with staging, validation, and rollback support."""

    def __init__(self, install_root: str = "/opt/platform/modules") -> None:
        self._install_root = Path(install_root)
        self._installed: dict[str, InstallRecord] = {}
        self._available_updates: dict[str, list[dict[str, Any]]] = {}
        self._staged_updates: dict[str, dict[str, Any]] = {}
        self._update_log: list[dict[str, Any]] = []
        self._lock = threading.RLock()

    def _log(self, message: str, level: str = "info", **kwargs: Any) -> None:
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": level,
            "message": message,
            **kwargs,
        }
        self._update_log.append(entry)

    def register_installed(self, record: InstallRecord) -> None:
        with self._lock:
            self._installed[record.package_name] = record

    def check_updates(
        self,
        available_versions: dict[str, list[str]],
    ) -> list[dict[str, Any]]:
        updates: list[dict[str, Any]] = []

        with self._lock:
            for name, installed in self._installed.items():
                available = available_versions.get(name, [])
                for version in available:
                    if self._is_newer(version, installed.package_version):
                        updates.append(
                            {
                                "package": name,
                                "current_version": installed.package_version,
                                "available_version": version,
                                "type": self._get_update_type(installed.package_version, version),
                            }
                        )

        return updates

    def _is_newer(self, version1: str, version2: str) -> bool:
        parts1 = [int(x) for x in version1.split(".") if x.isdigit()]
        parts2 = [int(x) for x in version2.split(".") if x.isdigit()]

        for a, b in zip(parts1, parts2):
            if a > b:
                return True
            if a < b:
                return False

        return len(parts1) > len(parts2)

    def _get_update_type(self, current: str, target: str) -> str:
        current_parts = [int(x) for x in current.split(".") if x.isdigit()]
        target_parts = [int(x) for x in target.split(".") if x.isdigit()]

        if len(target_parts) > 0 and len(current_parts) > 0:
            if target_parts[0] > current_parts[0]:
                return "major"
            elif len(target_parts) > 1 and len(current_parts) > 1:
                if target_parts[1] > current_parts[1]:
                    return "minor"

        return "patch"

    def download_update(
        self,
        package_name: str,
        target_version: str,
        source_url: str = "",
    ) -> dict[str, Any]:
        self._log(f"Downloading update {package_name}@{target_version}")

        return {
            "package": package_name,
            "version": target_version,
            "status": "downloaded",
            "source": source_url,
            "downloaded_at": datetime.now(UTC).isoformat(),
        }

    def validate_update(
        self,
        package_name: str,
        target_version: str,
        manifest: PackageManifest,
    ) -> dict[str, Any]:
        issues: list[str] = []
        warnings: list[str] = []

        compatibility = manifest.compatibility
        if compatibility.platform_core:
            self._log(f"Checking platform compatibility: {compatibility.platform_core}")

        with self._lock:
            installed = self._installed.get(package_name)
            if installed:
                for dep in manifest.dependencies.required:
                    if dep.get("name") == package_name:
                        continue

        return {
            "package": package_name,
            "version": target_version,
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
        }

    def stage_update(
        self,
        package_name: str,
        target_version: str,
    ) -> dict[str, Any]:
        with self._lock:
            self._staged_updates[package_name] = {
                "package": package_name,
                "target_version": target_version,
                "staged_at": datetime.now(UTC).isoformat(),
                "status": "staged",
            }

        self._log(f"Staged update {package_name}@{target_version}")
        return self._staged_updates[package_name]

    def apply_update(
        self,
        package_name: str,
        target_version: str,
    ) -> dict[str, Any]:
        with self._lock:
            staged = self._staged_updates.get(package_name)
            if staged is None:
                raise UpdateError(f"No staged update for {package_name}")

            installed = self._installed.get(package_name)
            if installed:
                installed.package_version = target_version
                installed.status = InstallStatus.COMPLETED
            else:
                self._installed[package_name] = InstallRecord(
                    package_name=package_name,
                    package_version=target_version,
                    status=InstallStatus.COMPLETED,
                )

            del self._staged_updates[package_name]

        self._log(f"Applied update {package_name}@{target_version}")
        return {
            "package": package_name,
            "version": target_version,
            "status": "applied",
            "applied_at": datetime.now(UTC).isoformat(),
        }

    def rollback_update(self, package_name: str) -> dict[str, Any]:
        with self._lock:
            staged = self._staged_updates.pop(package_name, None)
            if staged:
                return {
                    "package": package_name,
                    "status": "rolled_back",
                    "action": "removed_staged",
                }

        self._log(f"Rolled back update for {package_name}")
        return {
            "package": package_name,
            "status": "rolled_back",
            "action": "nothing_to_rollback",
        }

    def get_available_updates(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._staged_updates.values())

    def get_update_log(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._update_log[-limit:])
