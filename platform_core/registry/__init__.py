"""Module Registry - Centralized module/package registry."""

from __future__ import annotations

import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from platform_core.packages import (
    PackageCapabilities,
    PackageChecksum,
    PackageCompatibility,
    PackageDependencies,
    PackageLifecycle,
    PackageSignature,
    PackageStatus,
    PackageUUID,
    RegistryEntry,
)


class ModuleRegistry:
    """
    Centralized registry for modules, plugins, SDKs,
    templates, policies, workflows, and knowledge packs.
    """

    def __init__(self, storage_path: str | None = None) -> None:
        self._entries: dict[str, dict[str, RegistryEntry]] = {}
        self._storage_path = storage_path
        self._lock = threading.RLock()
        if storage_path:
            self._load_from_disk()

    def _load_from_disk(self) -> None:
        if not self._storage_path:
            return
        path = Path(self._storage_path)
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            for name, versions in data.items():
                self._entries[name] = {}
                for version, entry_data in versions.items():
                    self._entries[name][version] = self._entry_from_dict(entry_data)
        except Exception:
            pass

    def _save_to_disk(self) -> None:
        if not self._storage_path:
            return
        path = Path(self._storage_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data: dict[str, Any] = {}
        for name, versions in self._entries.items():
            data[name] = {}
            for version, entry in versions.items():
                data[name][version] = self._entry_to_dict(entry)
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    def _entry_to_dict(self, entry: RegistryEntry) -> dict[str, Any]:
        return {
            "uuid": str(entry.uuid),
            "name": entry.name,
            "version": entry.version,
            "publisher": entry.publisher,
            "license": entry.license,
            "status": entry.status.value,
            "created_at": entry.created_at.isoformat(),
            "updated_at": entry.updated_at.isoformat(),
            "dependencies": {
                "required": entry.dependencies.required,
                "optional": entry.dependencies.optional,
            },
            "capabilities": {
                "provides": entry.capabilities.provides,
                "requires": entry.capabilities.requires,
            },
            "compatibility": {
                "platform_core": entry.compatibility.platform_core,
                "runtime": entry.compatibility.runtime,
                "sdk_version": entry.compatibility.sdk_version,
            },
            "lifecycle": {
                "maturity": entry.lifecycle.maturity.value,
                "status": entry.lifecycle.status.value,
            },
            "checksum": {
                "algorithm": entry.checksum.algorithm,
                "value": entry.checksum.value,
            },
            "signature": {
                "algorithm": entry.signature.algorithm.value,
                "signature": entry.signature.signature,
                "signer": entry.signature.signer,
            },
        }

    def _entry_from_dict(self, data: dict[str, Any]) -> RegistryEntry:
        return RegistryEntry(
            uuid=PackageUUID(id=PackageUUID().id),
            name=data.get("name", ""),
            version=data.get("version", "0.1.0"),
            publisher=data.get("publisher", ""),
            license=data.get("license", "proprietary"),
            status=PackageStatus(data.get("status", "active")),
            created_at=datetime.fromisoformat(
                data.get("created_at", datetime.now(UTC).isoformat())
            ),
            updated_at=datetime.fromisoformat(
                data.get("updated_at", datetime.now(UTC).isoformat())
            ),
            dependencies=PackageDependencies(
                required=data.get("dependencies", {}).get("required", []),
                optional=data.get("dependencies", {}).get("optional", []),
            ),
            capabilities=PackageCapabilities(
                provides=data.get("capabilities", {}).get("provides", []),
                requires=data.get("capabilities", {}).get("requires", []),
            ),
            compatibility=PackageCompatibility(
                platform_core=data.get("compatibility", {}).get("platform_core", ">=1.0.0"),
                runtime=data.get("compatibility", {}).get("runtime", "python>=3.11"),
                sdk_version=data.get("compatibility", {}).get("sdk_version", ">=1.0.0"),
            ),
            lifecycle=PackageLifecycle(),
            checksum=PackageChecksum(
                algorithm=data.get("checksum", {}).get("algorithm", "sha256"),
                value=data.get("checksum", {}).get("value", ""),
            ),
            signature=PackageSignature(
                signature=data.get("signature", {}).get("signature", ""),
                signer=data.get("signature", {}).get("signer", ""),
            ),
        )

    def register(self, entry: RegistryEntry) -> None:
        with self._lock:
            if entry.name not in self._entries:
                self._entries[entry.name] = {}
            self._entries[entry.name][entry.version] = entry
            self._save_to_disk()

    def unregister(self, name: str, version: str) -> bool:
        with self._lock:
            if name in self._entries and version in self._entries[name]:
                del self._entries[name][version]
                if not self._entries[name]:
                    del self._entries[name]
                self._save_to_disk()
                return True
            return False

    def get(self, name: str, version: str | None = None) -> RegistryEntry | None:
        with self._lock:
            if name not in self._entries:
                return None
            if version:
                return self._entries[name].get(version)
            versions = self._entries[name]
            if versions:
                return list(versions.values())[-1]
            return None

    def list_packages(
        self,
        status: PackageStatus | None = None,
        category: str | None = None,
    ) -> list[RegistryEntry]:
        with self._lock:
            result = []
            for versions in self._entries.values():
                for entry in versions.values():
                    if status and entry.status != status:
                        continue
                    result.append(entry)
            return result

    def list_versions(self, name: str) -> list[str]:
        with self._lock:
            if name not in self._entries:
                return []
            return sorted(self._entries[name].keys())

    def search(self, query: str) -> list[RegistryEntry]:
        query_lower = query.lower()
        with self._lock:
            result = []
            for versions in self._entries.values():
                for entry in versions.values():
                    if (
                        query_lower in entry.name.lower()
                        or query_lower in entry.publisher.lower()
                        or any(query_lower in tag for tag in entry.capabilities.provides)
                    ):
                        result.append(entry)
            return result

    def get_latest_version(self, name: str) -> str | None:
        versions = self.list_versions(name)
        return versions[-1] if versions else None

    def package_exists(self, name: str, version: str | None = None) -> bool:
        with self._lock:
            if name not in self._entries:
                return False
            if version:
                return version in self._entries[name]
            return True

    def count(self) -> int:
        with self._lock:
            return sum(len(versions) for versions in self._entries.values())

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self._save_to_disk()
