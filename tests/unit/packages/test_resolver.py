"""Unit tests for Dependency Resolver."""

import pytest
from platform_core.resolver import (
    DependencyResolver,
    CircularDependencyError,
    VersionConflict,
)


class TestDependencyResolver:
    def test_init(self) -> None:
        resolver = DependencyResolver()
        assert resolver is not None

    def test_simple_resolve(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "b", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [])
        result = resolver.resolve("a", "1.0.0")
        assert len(result) == 2
        names = [r["name"] for r in result]
        assert "a" in names
        assert "b" in names

    def test_no_dependencies(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("leaf", "1.0.0", [])
        result = resolver.resolve("leaf", "1.0.0")
        assert len(result) == 1
        assert result[0]["name"] == "leaf"

    def test_circular_dependency(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "b", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [{"name": "a", "version": ">=1.0.0"}])
        with pytest.raises(CircularDependencyError):
            resolver.resolve("a", "1.0.0")

    def test_detect_cycles(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "b", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [{"name": "a", "version": ">=1.0.0"}])
        cycles = resolver.detect_cycles()
        assert len(cycles) > 0

    def test_no_cycles(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "b", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [])
        cycles = resolver.detect_cycles()
        assert len(cycles) == 0

    def test_dependency_tree(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "b", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [])
        tree = resolver.get_dependency_tree("a", "1.0.0")
        assert tree["name"] == "a"
        assert tree["version"] == "1.0.0"
        assert len(tree["dependencies"]) == 1

    def test_visualize_tree(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "b", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [])
        viz = resolver.visualize_tree("a", "1.0.0")
        assert "a@1.0.0" in viz
        assert "b@" in viz

    def test_detect_conflicts(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "c", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [{"name": "c", "version": ">=2.0.0"}])
        conflicts = resolver.detect_conflicts()
        assert len(conflicts) > 0

    def test_no_conflicts(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "b", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [])
        conflicts = resolver.detect_conflicts()
        assert len(conflicts) == 0

    def test_install_order(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "b", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [])
        order = resolver.get_install_order("a", "1.0.0")
        assert "a" in order
        assert "b" in order

    def test_compare_versions(self) -> None:
        resolver = DependencyResolver()
        assert resolver._compare_versions("1.0.0", "2.0.0") < 0
        assert resolver._compare_versions("2.0.0", "1.0.0") > 0
        assert resolver._compare_versions("1.0.0", "1.0.0") == 0

    def test_satisfies(self) -> None:
        resolver = DependencyResolver()
        assert resolver._satisfies("1.5.0", ">=1.0.0")
        assert not resolver._satisfies("0.9.0", ">=1.0.0")
        assert resolver._satisfies("1.0.0", "==1.0.0")
        assert resolver._satisfies("1.0.0", "")

    def test_deep_dependency_chain(self) -> None:
        resolver = DependencyResolver()
        resolver.add_package("a", "1.0.0", [{"name": "b", "version": ">=1.0.0"}])
        resolver.add_package("b", "1.0.0", [{"name": "c", "version": ">=1.0.0"}])
        resolver.add_package("c", "1.0.0", [])
        result = resolver.resolve("a", "1.0.0")
        assert len(result) == 3
        order = resolver.get_install_order("a", "1.0.0")
        assert set(order) == {"a", "b", "c"}
