"""Package REST API - Module, Registry, Repository, Update, Package APIs."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from typing import Any

from platform_core.packages.manager import PackageManager


class PackageAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Package Manager REST API."""

    _manager: PackageManager | None = None

    @classmethod
    def set_manager(cls, manager: PackageManager) -> None:
        cls._manager = manager

    def _get_manager(self) -> PackageManager:
        if self._manager is None:
            raise RuntimeError("Manager not initialized")
        return self._manager

    def _send_json(self, data: dict[str, Any], status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def _read_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        return json.loads(body)

    def do_GET(self) -> None:
        path = self.path.rstrip("/")

        if path == "/api/v1/health":
            self._send_json({"status": "healthy"})

        elif path == "/api/v1/modules":
            manager = self._get_manager()
            packages = manager.registry.list_packages()
            self._send_json({
                "modules": [
                    {"name": p.name, "version": p.version, "status": p.status.value}
                    for p in packages
                ]
            })

        elif path.startswith("/api/v1/modules/"):
            parts = path.split("/")
            name = parts[4] if len(parts) > 4 else ""
            version = parts[5] if len(parts) > 5 else None
            manager = self._get_manager()
            entry = manager.registry.get(name, version)
            if entry:
                self._send_json({
                    "name": entry.name,
                    "version": entry.version,
                    "publisher": entry.publisher,
                    "status": entry.status.value,
                })
            else:
                self._send_json({"error": "Not found"}, 404)

        elif path == "/api/v1/packages/installed":
            manager = self._get_manager()
            packages = manager.list_installed()
            self._send_json({"packages": packages})

        elif path == "/api/v1/repositories":
            manager = self._get_manager()
            repos = manager.repository_manager.list_repositories()
            self._send_json({
                "repositories": [
                    {"name": r.name, "type": r.type.value, "url": r.url, "enabled": r.enabled}
                    for r in repos
                ]
            })

        elif path == "/api/v1/doctor":
            manager = self._get_manager()
            result = manager.doctor()
            self._send_json(result)

        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self) -> None:
        path = self.path.rstrip("/")

        if path == "/api/v1/packages/install":
            body = self._read_body()
            manager = self._get_manager()
            result = manager.install(
                package_name=body.get("package", ""),
                version=body.get("version", ""),
                dry_run=body.get("dry_run", False),
            )
            self._send_json(result)

        elif path == "/api/v1/packages/uninstall":
            body = self._read_body()
            manager = self._get_manager()
            result = manager.uninstall(body.get("package", ""))
            self._send_json(result)

        elif path == "/api/v1/packages/update":
            body = self._read_body()
            manager = self._get_manager()
            result = manager.update(
                package_name=body.get("package", ""),
                target_version=body.get("version", ""),
            )
            self._send_json(result)

        elif path == "/api/v1/packages/verify":
            body = self._read_body()
            manager = self._get_manager()
            result = manager.verify(body.get("package", ""))
            self._send_json(result)

        elif path == "/api/v1/packages/rollback":
            body = self._read_body()
            manager = self._get_manager()
            result = manager.rollback(body.get("package", ""))
            self._send_json(result)

        elif path == "/api/v1/packages/repair":
            body = self._read_body()
            manager = self._get_manager()
            result = manager.repair(body.get("package", ""))
            self._send_json(result)

        elif path == "/api/v1/modules":
            body = self._read_body()
            manager = self._get_manager()
            from platform_core.packages import RegistryEntry, PackageStatus

            entry = RegistryEntry(
                name=body.get("name", ""),
                version=body.get("version", "0.1.0"),
                publisher=body.get("publisher", ""),
                status=PackageStatus(body.get("status", "active")),
            )
            manager.registry.register(entry)
            self._send_json({"status": "registered", "name": entry.name})

        elif path == "/api/v1/repositories":
            body = self._read_body()
            manager = self._get_manager()
            from platform_core.packages import RepositoryConfig, RepositoryType

            config = RepositoryConfig(
                name=body.get("name", ""),
                type=RepositoryType(body.get("type", "local")),
                url=body.get("url", ""),
                enabled=body.get("enabled", True),
            )
            manager.repository_manager.add_repository(config)
            self._send_json({"status": "added", "name": config.name})

        else:
            self._send_json({"error": "Not found"}, 404)

    def do_DELETE(self) -> None:
        path = self.path.rstrip("/")

        if path.startswith("/api/v1/modules/"):
            parts = path.split("/")
            name = parts[4] if len(parts) > 4 else ""
            version = parts[5] if len(parts) > 5 else None
            manager = self._get_manager()
            if version:
                success = manager.registry.unregister(name, version)
            else:
                success = False
            self._send_json({"deleted": success})

        elif path.startswith("/api/v1/repositories/"):
            parts = path.split("/")
            name = parts[4] if len(parts) > 4 else ""
            manager = self._get_manager()
            success = manager.repository_manager.remove_repository(name)
            self._send_json({"deleted": success})

        else:
            self._send_json({"error": "Not found"}, 404)

    def log_message(self, format: str, *args: Any) -> None:
        pass
