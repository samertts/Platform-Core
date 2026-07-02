from __future__ import annotations

import importlib
import importlib.util
import logging
import sys
import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger("platform_core.plugins")


@dataclass
class PluginInfo:
    id: str
    name: str
    version: str
    status: str
    path: str
    description: str = ""
    author: str = ""
    dependencies: list[str] = field(default_factory=list)
    min_platform_version: str = "1.0.0"
    max_platform_version: str = ""
    activated_at: datetime | None = None
    error: str | None = None


class PluginEngine:
    """Plugin discovery, loading, isolation, and lifecycle management."""

    def __init__(self, platform_version: str = "1.0.0") -> None:
        self._plugins: dict[str, PluginInfo] = {}
        self._plugin_modules: dict[str, Any] = {}
        self._plugin_instances: dict[str, Any] = {}
        self._platform_version = platform_version
        self._lock = threading.RLock()
        self._load_order: list[str] = []

    async def discover(self, paths: list[str]) -> list[str]:
        discovered: list[str] = []
        for path_str in paths:
            path = Path(path_str)
            if not path.exists():
                continue

            if path.is_file() and path.suffix == ".py":
                plugin_id = self._discover_plugin_from_file(path)
                if plugin_id:
                    discovered.append(plugin_id)
            elif path.is_dir():
                for plugin_file in sorted(path.glob("*.py")):
                    if plugin_file.name.startswith("_"):
                        continue
                    plugin_id = self._discover_plugin_from_file(plugin_file)
                    if plugin_id:
                        discovered.append(plugin_id)

                for plugin_dir in sorted(path.iterdir()):
                    if plugin_dir.is_dir() and not plugin_dir.name.startswith("_"):
                        init_file = plugin_dir / "__init__.py"
                        if init_file.exists():
                            plugin_id = self._discover_plugin_from_dir(plugin_dir)
                            if plugin_id:
                                discovered.append(plugin_id)

        return discovered

    def _discover_plugin_from_file(self, path: Path) -> str | None:
        try:
            spec = importlib.util.spec_from_file_location(
                f"platform_core_plugin_{path.stem}", str(path)
            )
            if spec is None or spec.loader is None:
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            plugin_id = getattr(module, "PLUGIN_ID", path.stem)
            plugin_version = getattr(module, "PLUGIN_VERSION", "0.1.0")
            plugin_name = getattr(module, "PLUGIN_NAME", plugin_id)
            plugin_desc = getattr(module, "PLUGIN_DESCRIPTION", "")
            plugin_author = getattr(module, "PLUGIN_AUTHOR", "")
            plugin_deps = getattr(module, "PLUGIN_DEPENDENCIES", [])
            min_ver = getattr(module, "MIN_PLATFORM_VERSION", "1.0.0")
            max_ver = getattr(module, "MAX_PLATFORM_VERSION", "")

            info = PluginInfo(
                id=plugin_id,
                name=plugin_name,
                version=plugin_version,
                status="discovered",
                path=str(path),
                description=plugin_desc,
                author=plugin_author,
                dependencies=plugin_deps,
                min_platform_version=min_ver,
                max_platform_version=max_ver,
            )

            with self._lock:
                self._plugins[plugin_id] = info
                self._plugin_modules[plugin_id] = module

            return plugin_id
        except Exception as e:
            logger.warning("Failed to discover plugin %s: %s", path, e)
            return None

    def _discover_plugin_from_dir(self, path: Path) -> str | None:
        try:
            module_name = f"platform_core_plugin_{path.name}"
            spec = importlib.util.spec_from_file_location(module_name, str(path / "__init__.py"))
            if spec is None or spec.loader is None:
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            plugin_id = getattr(module, "PLUGIN_ID", path.name)
            plugin_version = getattr(module, "PLUGIN_VERSION", "0.1.0")
            plugin_name = getattr(module, "PLUGIN_NAME", plugin_id)

            info = PluginInfo(
                id=plugin_id,
                name=plugin_name,
                version=plugin_version,
                status="discovered",
                path=str(path),
            )

            with self._lock:
                self._plugins[plugin_id] = info
                self._plugin_modules[plugin_id] = module

            return plugin_id
        except Exception as e:
            logger.warning("Failed to discover plugin dir %s: %s", path, e)
            return None

    async def load(self, plugin_id: str) -> None:
        with self._lock:
            info = self._plugins.get(plugin_id)
            if info is None:
                raise ValueError(f"Plugin not found: {plugin_id}")

            errors = self.validate_compatibility(plugin_id)
            if errors:
                info.status = "error"
                info.error = "; ".join(errors)
                raise ValueError(f"Plugin {plugin_id} incompatible: {errors}")

            for dep in info.dependencies:
                dep_info = self._plugins.get(dep)
                if dep_info is None or dep_info.status not in ("loaded", "active"):
                    info.status = "error"
                    info.error = f"Missing dependency: {dep}"
                    raise ValueError(f"Plugin {plugin_id} missing dependency: {dep}")

            module = self._plugin_modules.get(plugin_id)
            if module is None:
                info.status = "error"
                info.error = "Module not loaded"
                raise ValueError(f"Plugin {plugin_id} module not found")

            plugin_class = getattr(module, "Plugin", None)
            if plugin_class is None:
                info.status = "error"
                info.error = "No Plugin class found"
                raise ValueError(f"Plugin {plugin_id} has no Plugin class")

            try:
                instance = plugin_class()
                self._plugin_instances[plugin_id] = instance
                info.status = "loaded"
                self._load_order.append(plugin_id)
            except Exception as e:
                info.status = "error"
                info.error = str(e)
                raise

    async def activate(self, plugin_id: str) -> None:
        with self._lock:
            info = self._plugins.get(plugin_id)
            if info is None:
                raise ValueError(f"Plugin not found: {plugin_id}")
            if info.status != "loaded":
                raise ValueError(f"Plugin {plugin_id} not loaded (status: {info.status})")

            instance = self._plugin_instances.get(plugin_id)
            if instance is not None and hasattr(instance, "activate"):
                try:
                    await instance.activate()
                except Exception as e:
                    info.status = "error"
                    info.error = str(e)
                    raise

            info.status = "active"
            info.activated_at = datetime.now(UTC)

    async def deactivate(self, plugin_id: str) -> None:
        with self._lock:
            info = self._plugins.get(plugin_id)
            if info is None:
                raise ValueError(f"Plugin not found: {plugin_id}")

            instance = self._plugin_instances.get(plugin_id)
            if instance is not None and hasattr(instance, "deactivate"):
                try:
                    await instance.deactivate()
                except Exception:
                    pass

            info.status = "loaded"
            info.activated_at = None

    async def unload(self, plugin_id: str) -> None:
        await self.deactivate(plugin_id)
        with self._lock:
            info = self._plugins.get(plugin_id)
            if info:
                info.status = "unloaded"
            self._plugin_instances.pop(plugin_id, None)
            self._plugin_modules.pop(plugin_id, None)
            if plugin_id in self._load_order:
                self._load_order.remove(plugin_id)

    def get_plugin(self, plugin_id: str) -> Any:
        with self._lock:
            return self._plugin_instances.get(plugin_id)

    def list_plugins(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "id": p.id,
                    "name": p.name,
                    "version": p.version,
                    "status": p.status,
                    "path": p.path,
                    "description": p.description,
                    "error": p.error,
                    "activated_at": (p.activated_at.isoformat() if p.activated_at else None),
                }
                for p in self._plugins.values()
            ]

    def validate_compatibility(self, plugin_id: str) -> list[str]:
        errors: list[str] = []
        with self._lock:
            info = self._plugins.get(plugin_id)
            if info is None:
                return [f"Plugin {plugin_id} not found"]

            if info.min_platform_version:
                if self._compare_versions(self._platform_version, info.min_platform_version) < 0:
                    errors.append(
                        f"Platform version {self._platform_version} < required {info.min_platform_version}"
                    )

            if info.max_platform_version:
                if self._compare_versions(self._platform_version, info.max_platform_version) > 0:
                    errors.append(
                        f"Platform version {self._platform_version} > maximum {info.max_platform_version}"
                    )

        return errors

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

    @property
    def plugin_count(self) -> int:
        with self._lock:
            return len(self._plugins)

    @property
    def active_count(self) -> int:
        with self._lock:
            return sum(1 for p in self._plugins.values() if p.status == "active")
