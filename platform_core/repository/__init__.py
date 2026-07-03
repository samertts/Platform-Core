"""Repository Manager - Local, remote, mirror, offline, government repositories."""

from __future__ import annotations

import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from platform_core.packages import RegistryEntry, RepositoryConfig, RepositoryType


class RepositoryError(Exception):
    pass


class RepositoryManager:
    """Manages package repositories with priority-based resolution."""

    REPOSITORY_PRIORITY = {
        RepositoryType.LOCAL: 100,
        RepositoryType.GOVERNMENT: 90,
        RepositoryType.OFFLINE: 80,
        RepositoryType.MIRROR: 50,
        RepositoryType.REMOTE: 10,
    }

    def __init__(self, config_path: str | None = None) -> None:
        self._repositories: dict[str, RepositoryConfig] = {}
        self._package_cache: dict[str, dict[str, list[RegistryEntry]]] = {}
        self._config_path = config_path
        self._lock = threading.RLock()
        if config_path:
            self._load_config()

    def _load_config(self) -> None:
        if not self._config_path:
            return
        path = Path(self._config_path)
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            for name, repo_data in data.get("repositories", {}).items():
                self._repositories[name] = RepositoryConfig(
                    name=name,
                    type=RepositoryType(repo_data.get("type", "local")),
                    url=repo_data.get("url", ""),
                    priority=repo_data.get("priority", 0),
                    enabled=repo_data.get("enabled", True),
                    trusted=repo_data.get("trusted", False),
                    mirror_of=repo_data.get("mirror_of", ""),
                )
        except Exception:
            pass

    def _save_config(self) -> None:
        if not self._config_path:
            return
        path = Path(self._config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {"repositories": {}}
        for name, repo in self._repositories.items():
            data["repositories"][name] = {
                "type": repo.type.value,
                "url": repo.url,
                "priority": repo.priority,
                "enabled": repo.enabled,
                "trusted": repo.trusted,
                "mirror_of": repo.mirror_of,
            }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add_repository(self, config: RepositoryConfig) -> None:
        with self._lock:
            if not config.priority:
                config.priority = self.REPOSITORY_PRIORITY.get(config.type, 0)
            self._repositories[config.name] = config
            self._save_config()

    def remove_repository(self, name: str) -> bool:
        with self._lock:
            if name in self._repositories:
                del self._repositories[name]
                self._package_cache.pop(name, None)
                self._save_config()
                return True
            return False

    def get_repository(self, name: str) -> RepositoryConfig | None:
        with self._lock:
            return self._repositories.get(name)

    def list_repositories(
        self,
        type_filter: RepositoryType | None = None,
        enabled_only: bool = True,
    ) -> list[RepositoryConfig]:
        with self._lock:
            result = []
            for repo in self._repositories.values():
                if enabled_only and not repo.enabled:
                    continue
                if type_filter and repo.type != type_filter:
                    continue
                result.append(repo)
            return sorted(result, key=lambda r: r.priority, reverse=True)

    def register_package(self, repo_name: str, entry: RegistryEntry) -> None:
        with self._lock:
            if repo_name not in self._package_cache:
                self._package_cache[repo_name] = {}
            if entry.name not in self._package_cache[repo_name]:
                self._package_cache[repo_name][entry.name] = []
            self._package_cache[repo_name][entry.name].append(entry)

    def find_package(
        self,
        name: str,
        version_constraint: str = "*",
    ) -> list[tuple[RepositoryConfig, RegistryEntry]]:
        results: list[tuple[RepositoryConfig, RegistryEntry]] = []
        repos = self.list_repositories(enabled_only=True)

        for repo in repos:
            cached = self._package_cache.get(repo.name, {}).get(name, [])
            for entry in cached:
                results.append((repo, entry))

        return results

    def get_package_from_priority(
        self,
        name: str,
        version_constraint: str = "*",
    ) -> tuple[RepositoryConfig, RegistryEntry] | None:
        repos = self.list_repositories(enabled_only=True)

        for repo in repos:
            cached = self._package_cache.get(repo.name, {}).get(name, [])
            if cached:
                return (repo, cached[-1])

        return None

    def resolve_package(
        self,
        name: str,
        version_constraint: str = "*",
    ) -> RegistryEntry | None:
        result = self.get_package_from_priority(name, version_constraint)
        return result[1] if result else None

    def sync_repository(self, name: str) -> dict[str, Any]:
        repo = self.get_repository(name)
        if repo is None:
            raise RepositoryError(f"Repository not found: {name}")

        repo.last_synced = datetime.now(UTC)
        self._save_config()

        return {
            "repository": name,
            "synced_at": repo.last_synced.isoformat(),
            "status": "synced",
        }

    def get_repository_stats(self) -> dict[str, Any]:
        stats: dict[str, Any] = {
            "total_repositories": 0,
            "enabled_repositories": 0,
            "by_type": {},
            "total_cached_packages": 0,
        }

        with self._lock:
            stats["total_repositories"] = len(self._repositories)
            stats["enabled_repositories"] = sum(1 for r in self._repositories.values() if r.enabled)

            for repo in self._repositories.values():
                repo_type = repo.type.value
                stats["by_type"][repo_type] = stats["by_type"].get(repo_type, 0) + 1

            for repo_packages in self._package_cache.values():
                for versions in repo_packages.values():
                    stats["total_cached_packages"] += len(versions)

        return stats
