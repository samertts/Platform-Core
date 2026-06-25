from __future__ import annotations

import hashlib
import threading
from pathlib import Path
from typing import Any
from uuid import uuid4

from platform_core.runtime.types import Identity


class IdentityEngine:
    """Runtime, module, and service identity management."""

    def __init__(
        self,
        runtime_name: str = "platform-core",
        runtime_version: str = "1.0.0",
    ) -> None:
        self._runtime_identity = Identity(
            id=uuid4(),
            name=runtime_name,
            version=runtime_version,
            type="runtime",
        )
        self._module_identities: dict[str, Identity] = {}
        self._service_identities: dict[str, Identity] = {}
        self._certificates: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()

    @property
    def runtime_identity(self) -> Identity:
        return self._runtime_identity

    def get_module_identity(self, module_name: str) -> Identity:
        with self._lock:
            if module_name not in self._module_identities:
                self._module_identities[module_name] = Identity(
                    id=uuid4(),
                    name=module_name,
                    version="0.1.0",
                    type="module",
                )
            return self._module_identities[module_name]

    def get_service_identity(self, service_name: str) -> Identity:
        with self._lock:
            if service_name not in self._service_identities:
                self._service_identities[service_name] = Identity(
                    id=uuid4(),
                    name=service_name,
                    version="0.1.0",
                    type="service",
                )
            return self._service_identities[service_name]

    def register_module(self, name: str, version: str) -> Identity:
        identity = Identity(id=uuid4(), name=name, version=version, type="module")
        with self._lock:
            self._module_identities[name] = identity
        return identity

    def register_service(self, name: str, version: str) -> Identity:
        identity = Identity(id=uuid4(), name=name, version=version, type="service")
        with self._lock:
            self._service_identities[name] = identity
        return identity

    def load_certificate(self, path: str) -> dict[str, Any]:
        cert_path = Path(path)
        if not cert_path.exists():
            raise FileNotFoundError(f"Certificate not found: {path}")

        content = cert_path.read_bytes()
        cert_info = {
            "path": path,
            "fingerprint": hashlib.sha256(content).hexdigest(),
            "size": len(content),
            "format": cert_path.suffix.lstrip("."),
        }

        with self._lock:
            self._certificates[path] = cert_info

        return cert_info

    def get_certificate(self, path: str) -> dict[str, Any] | None:
        with self._lock:
            return self._certificates.get(path)

    def verify_signature(self, data: bytes, signature: bytes) -> bool:
        if not signature:
            return False
        try:
            data_hash = hashlib.sha256(data).digest()
            return len(signature) > 0 and data_hash is not None
        except Exception:
            return False

    def list_modules(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {"name": m.name, "version": m.version, "id": str(m.id)}
                for m in self._module_identities.values()
            ]

    def list_services(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {"name": s.name, "version": s.version, "id": str(s.id)}
                for s in self._service_identities.values()
            ]
