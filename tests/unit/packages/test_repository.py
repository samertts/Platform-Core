"""Unit tests for Repository Manager."""

import pytest

from platform_core.packages import RegistryEntry, RepositoryConfig, RepositoryType
from platform_core.repository import RepositoryError, RepositoryManager


class TestRepositoryManager:
    def test_init(self) -> None:
        manager = RepositoryManager()
        assert manager is not None

    def test_add_repository(self) -> None:
        manager = RepositoryManager()
        config = RepositoryConfig(name="test", type=RepositoryType.LOCAL, url="/test")
        manager.add_repository(config)
        repos = manager.list_repositories()
        assert len(repos) == 1

    def test_remove_repository(self) -> None:
        manager = RepositoryManager()
        config = RepositoryConfig(name="test", type=RepositoryType.LOCAL)
        manager.add_repository(config)
        assert manager.remove_repository("test")
        assert len(manager.list_repositories()) == 0

    def test_remove_nonexistent(self) -> None:
        manager = RepositoryManager()
        assert not manager.remove_repository("nonexistent")

    def test_get_repository(self) -> None:
        manager = RepositoryManager()
        config = RepositoryConfig(name="test", type=RepositoryType.LOCAL)
        manager.add_repository(config)
        repo = manager.get_repository("test")
        assert repo is not None
        assert repo.name == "test"

    def test_list_repositories(self) -> None:
        manager = RepositoryManager()
        manager.add_repository(RepositoryConfig(name="a", type=RepositoryType.LOCAL))
        manager.add_repository(RepositoryConfig(name="b", type=RepositoryType.REMOTE))
        repos = manager.list_repositories()
        assert len(repos) == 2

    def test_list_repositories_by_type(self) -> None:
        manager = RepositoryManager()
        manager.add_repository(RepositoryConfig(name="local", type=RepositoryType.LOCAL))
        manager.add_repository(RepositoryConfig(name="remote", type=RepositoryType.REMOTE))
        local_repos = manager.list_repositories(type_filter=RepositoryType.LOCAL)
        assert len(local_repos) == 1

    def test_register_package(self) -> None:
        manager = RepositoryManager()
        manager.add_repository(RepositoryConfig(name="test", type=RepositoryType.LOCAL))
        entry = RegistryEntry(name="pkg", version="1.0.0")
        manager.register_package("test", entry)
        results = manager.find_package("pkg")
        assert len(results) == 1

    def test_resolve_package(self) -> None:
        manager = RepositoryManager()
        manager.add_repository(RepositoryConfig(name="test", type=RepositoryType.LOCAL))
        entry = RegistryEntry(name="pkg", version="1.0.0")
        manager.register_package("test", entry)
        result = manager.resolve_package("pkg")
        assert result is not None
        assert result.name == "pkg"

    def test_repository_stats(self) -> None:
        manager = RepositoryManager()
        manager.add_repository(RepositoryConfig(name="test", type=RepositoryType.LOCAL))
        stats = manager.get_repository_stats()
        assert stats["total_repositories"] == 1

    def test_sync_repository(self) -> None:
        manager = RepositoryManager()
        manager.add_repository(RepositoryConfig(name="test", type=RepositoryType.LOCAL))
        result = manager.sync_repository("test")
        assert result["status"] == "synced"

    def test_sync_nonexistent(self) -> None:
        manager = RepositoryManager()
        with pytest.raises(RepositoryError):
            manager.sync_repository("nonexistent")

    def test_get_package_from_priority(self) -> None:
        manager = RepositoryManager()
        manager.add_repository(
            RepositoryConfig(name="test", type=RepositoryType.LOCAL, priority=10)
        )
        entry = RegistryEntry(name="pkg", version="1.0.0")
        manager.register_package("test", entry)
        result = manager.get_package_from_priority("pkg", "1.0.0")
        assert result is not None
