from __future__ import annotations

import json
import os
import threading
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

from platform_core.runtime.config.schema import ConfigSchema


class ConfigurationEngine:
    """Hierarchical, hot-reloadable configuration engine.

    Supports:
    - Environment variable loading
    - File-based configuration (YAML/JSON)
    - Hierarchical merging (defaults < file < env)
    - Schema validation
    - Hot reload with file watching
    - Change callbacks
    """

    def __init__(self, schema: ConfigSchema | None = None) -> None:
        self._config: dict[str, Any] = {}
        self._schema = schema or ConfigSchema()
        self._sources: list[str] = []
        self._callbacks: dict[str, list[Callable[[str, Any, Any], None]]] = defaultdict(list)
        self._global_callbacks: list[Callable[[str, Any, Any], None]] = []
        self._lock = threading.RLock()
        self._file_mtimes: dict[str, float] = {}
        self._loaded = False

    async def load(self, sources: list[str]) -> None:
        """Load configuration from sources.

        Sources can be:
        - Environment variable prefix (e.g., "PLATFORM_")
        - File paths (e.g., "config.yaml", "config.json")
        - Directory paths (loads all config files in directory)
        """
        with self._lock:
            self._sources = sources
            base_config: dict[str, Any] = {}

            for source in sources:
                if os.path.isdir(source):
                    base_config = self._load_directory(source, base_config)
                elif os.path.isfile(source):
                    base_config = self._load_file(source, base_config)
                elif source.isupper() or "_" in source:
                    base_config = self._load_env_prefix(source, base_config)
                else:
                    base_config = self._load_env_prefix(source, base_config)

            self._config = base_config
            self._loaded = True

    def _load_env_prefix(self, prefix: str, base: dict[str, Any]) -> dict[str, Any]:
        result = dict(base)
        prefix_lower = prefix.lower()
        for key, value in os.environ.items():
            key_lower = key.lower()
            if key_lower.startswith(prefix_lower):
                config_key = key_lower[len(prefix_lower) :].lstrip("_")
                if config_key:
                    parts = config_key.split("_")
                    current = result
                    for part in parts[:-1]:
                        current = current.setdefault(part, {})
                    current[parts[-1]] = self._parse_env_value(value)
        return result

    def _load_file(self, file_path: str, base: dict[str, Any]) -> dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            return base

        try:
            content = path.read_text(encoding="utf-8")
            if path.suffix in (".yaml", ".yml"):
                file_config = self._parse_yaml(content)
            elif path.suffix == ".json":
                file_config = json.loads(content)
            else:
                return base

            self._file_mtimes[file_path] = path.stat().st_mtime
            return self._deep_merge(base, file_config)
        except Exception:
            return base

    def _load_directory(self, dir_path: str, base: dict[str, Any]) -> dict[str, Any]:
        result = dict(base)
        path = Path(dir_path)
        if not path.exists():
            return result

        for file_path in sorted(path.glob("*.yaml")):
            result = self._load_file(str(file_path), result)
        for file_path in sorted(path.glob("*.yml")):
            result = self._load_file(str(file_path), result)
        for file_path in sorted(path.glob("*.json")):
            result = self._load_file(str(file_path), result)

        return result

    def _parse_yaml(self, content: str) -> dict[str, Any]:
        try:
            import yaml

            result = yaml.safe_load(content)
            return result if isinstance(result, dict) else {}
        except ImportError:
            return self._parse_simple_yaml(content)

    def _parse_simple_yaml(self, content: str) -> dict[str, Any]:
        result: dict[str, Any] = {}
        current_section: dict[str, Any] = result
        section_stack: list[tuple[int, dict[str, Any]]] = [(0, result)]

        for line in content.splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue

            indent = len(line) - len(line.lstrip())
            stripped = line.strip()

            while section_stack and indent <= section_stack[-1][0] and len(section_stack) > 1:
                section_stack.pop()
            current_section = section_stack[-1][1]

            if ":" in stripped:
                key, _, value = stripped.partition(":")
                key = key.strip()
                value = value.strip()

                if value:
                    current_section[key] = self._parse_yaml_value(value)
                else:
                    new_section: dict[str, Any] = {}
                    current_section[key] = new_section
                    section_stack.append((indent, new_section))

        return result

    def _parse_yaml_value(self, value: str) -> Any:
        if value.lower() in ("true", "yes", "on"):
            return True
        if value.lower() in ("false", "no", "off"):
            return False
        if value.lower() in ("null", "none"):
            return None
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            return value[1:-1]
        return value

    def _parse_env_value(self, value: str) -> Any:
        if value.lower() in ("true", "yes"):
            return True
        if value.lower() in ("false", "no"):
            return False
        if value.lower() in ("null", "none"):
            return None
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        return value

    def _deep_merge(self, base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        result = dict(base)
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            keys = key.split(".")
            current: Any = self._config
            for k in keys:
                if isinstance(current, dict):
                    current = current.get(k)
                    if current is None:
                        return default
                else:
                    return default
            return current

    def get_section(self, section: str) -> dict[str, Any]:
        with self._lock:
            keys = section.split(".")
            current = self._config
            for k in keys:
                if isinstance(current, dict):
                    current = current.get(k, {})
                else:
                    return {}
            return dict(current) if isinstance(current, dict) else {}

    async def reload(self) -> None:
        """Hot-reload configuration from original sources."""
        with self._lock:
            old_config = dict(self._config)

        await self.load(self._sources)

        with self._lock:
            new_config = dict(self._config)

        changes = self._find_changes(old_config, new_config)
        for key, old_val, new_val in changes:
            self._notify_callbacks(key, old_val, new_val)

    def _find_changes(
        self, old: dict[str, Any], new: dict[str, Any], prefix: str = ""
    ) -> list[tuple[str, Any, Any]]:
        changes: list[tuple[str, Any, Any]] = []
        all_keys = set(list(old.keys()) + list(new.keys()))

        for key in all_keys:
            full_key = f"{prefix}.{key}" if prefix else key
            old_val = old.get(key)
            new_val = new.get(key)

            if isinstance(old_val, dict) and isinstance(new_val, dict):
                changes.extend(self._find_changes(old_val, new_val, full_key))
            elif old_val != new_val:
                changes.append((full_key, old_val, new_val))

        return changes

    def _notify_callbacks(self, key: str, old_val: Any, new_val: Any) -> None:
        for callback in self._global_callbacks:
            try:
                callback(key, old_val, new_val)
            except Exception:
                pass

        for pattern, callbacks in self._callbacks.items():
            if key.startswith(pattern) or pattern == "*":
                for callback in callbacks:
                    try:
                        callback(key, old_val, new_val)
                    except Exception:
                        pass

    def watch(self, key: str, callback: Callable[[str, Any, Any], None]) -> None:
        with self._lock:
            self._callbacks[key].append(callback)

    def watch_all(self, callback: Callable[[str, Any, Any], None]) -> None:
        with self._lock:
            self._global_callbacks.append(callback)

    def validate(self) -> list[str]:
        with self._lock:
            return self._schema.validate(self._config)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            keys = key.split(".")
            current = self._config
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            old_value = current.get(keys[-1])
            current[keys[-1]] = value

        self._notify_callbacks(key, old_value, value)

    @property
    def schema(self) -> dict[str, Any]:
        return {
            field.name: {
                "type": field.type.__name__,
                "required": field.required,
                "default": field.default,
                "description": field.description,
            }
            for field in self._schema.fields.values()
        }

    @property
    def all(self) -> dict[str, Any]:
        with self._lock:
            return dict(self._config)

    @property
    def sources(self) -> list[str]:
        return list(self._sources)

    @property
    def loaded(self) -> bool:
        return self._loaded
