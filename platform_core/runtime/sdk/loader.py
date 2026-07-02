from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class SDKInfo:
    id: str
    version: str
    capabilities: list[str]
    loaded_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


class SDKLoader:
    """SDK registration, version negotiation, and capability discovery."""

    def __init__(self) -> None:
        self._sdks: dict[str, SDKInfo] = {}
        self._sdk_instances: dict[str, Any] = {}
        self._lock = threading.RLock()

    def register(self, sdk_id: str, sdk: Any) -> None:
        version = getattr(sdk, "VERSION", "0.1.0")
        capabilities = getattr(sdk, "CAPABILITIES", [])
        metadata = getattr(sdk, "METADATA", {})

        info = SDKInfo(
            id=sdk_id,
            version=version,
            capabilities=capabilities,
            metadata=metadata,
        )

        with self._lock:
            self._sdks[sdk_id] = info
            self._sdk_instances[sdk_id] = sdk

    def negotiate_version(self, sdk_id: str, required_version: str) -> str:
        with self._lock:
            info = self._sdks.get(sdk_id)
            if info is None:
                raise ValueError(f"SDK not registered: {sdk_id}")

            if self._is_compatible(info.version, required_version):
                return info.version

            raise ValueError(
                f"SDK {sdk_id} version {info.version} is not compatible with required {required_version}"
            )

    def _is_compatible(self, actual: str, required: str) -> bool:
        required = required.strip()
        if required.startswith(">="):
            min_version = required[2:].strip()
            return self._compare_versions(actual, min_version) >= 0
        elif required.startswith("^"):
            target = required[1:].strip()
            actual_parts = [int(x) for x in actual.split(".") if x.isdigit()]
            target_parts = [int(x) for x in target.split(".") if x.isdigit()]

            if len(actual_parts) < 1 or len(target_parts) < 1:
                return False

            if actual_parts[0] != target_parts[0]:
                return False

            return self._compare_versions(actual, target) >= 0
        else:
            return actual == required

    def _compare_versions(self, v1: str, v2: str) -> int:
        parts1 = [int(x) for x in v1.split(".") if x.isdigit()]
        parts2 = [int(x) for x in v2.split(".") if x.isdigit()]

        for a, b in zip(parts1, parts2):
            if a < b:
                return -1
            if a > b:
                return 1

        if len(parts1) < len(parts2):
            return -1
        if len(parts1) > len(parts2):
            return 1
        return 0

    def get_capabilities(self, sdk_id: str) -> list[str]:
        with self._lock:
            info = self._sdks.get(sdk_id)
            if info is None:
                raise ValueError(f"SDK not registered: {sdk_id}")
            return list(info.capabilities)

    def get_sdk(self, sdk_id: str) -> Any:
        with self._lock:
            return self._sdk_instances.get(sdk_id)

    def list_sdks(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "id": sdk.id,
                    "version": sdk.version,
                    "capabilities": sdk.capabilities,
                    "loaded_at": sdk.loaded_at.isoformat(),
                    "metadata": sdk.metadata,
                }
                for sdk in self._sdks.values()
            ]

    def unregister(self, sdk_id: str) -> bool:
        with self._lock:
            if sdk_id in self._sdks:
                del self._sdks[sdk_id]
                self._sdk_instances.pop(sdk_id, None)
                return True
            return False

    @property
    def sdk_count(self) -> int:
        with self._lock:
            return len(self._sdks)
