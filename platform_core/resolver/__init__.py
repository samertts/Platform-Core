"""Dependency Resolver - Graph-based dependency resolution with semver support."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any


class VersionConflict(Exception):
    def __init__(self, package: str, required: str, installed: str) -> None:
        self.package = package
        self.required = required
        self.installed = installed
        super().__init__(
            f"Version conflict for {package}: required {required}, installed {installed}"
        )


class CircularDependencyError(Exception):
    def __init__(self, chain: list[str]) -> None:
        self.chain = chain
        super().__init__(f"Circular dependency: {' -> '.join(chain)}")


class DependencyResolver:
    """Resolves dependencies using semantic versioning with conflict and cycle detection."""

    VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$")
    OPERATOR_PATTERN = re.compile(r"^(>=|<=|!=|==|\^|~|>|<)(.+)$")

    def __init__(self) -> None:
        self._graph: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self._resolved: dict[str, str] = {}

    def _parse_version(self, version: str) -> tuple[int, int, int, str | None]:
        match = self.VERSION_PATTERN.match(version)
        if not match:
            return (0, 0, 0, version)
        major, minor, patch = (
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
        )
        pre = match.group(4)
        return (major, minor, patch, pre)

    def _compare_versions(self, v1: str, v2: str) -> int:
        parts1 = self._parse_version(v1)[:3]
        parts2 = self._parse_version(v2)[:3]
        for a, b in zip(parts1, parts2):
            if a < b:
                return -1
            if a > b:
                return 1
        return 0

    def _satisfies(self, version: str, constraint: str) -> bool:
        constraint = constraint.strip()
        if not constraint:
            return True

        if constraint.startswith(">="):
            return self._compare_versions(version, constraint[2:].strip()) >= 0
        elif constraint.startswith("<="):
            return self._compare_versions(version, constraint[2:].strip()) <= 0
        elif constraint.startswith("!="):
            return self._compare_versions(version, constraint[2:].strip()) != 0
        elif constraint.startswith("^"):
            target = constraint[1:].strip()
            v_parts = self._parse_version(version)[:3]
            t_parts = self._parse_version(target)[:3]
            if v_parts[0] != t_parts[0]:
                return False
            return self._compare_versions(version, target) >= 0
        elif constraint.startswith("~"):
            target = constraint[1:].strip()
            v_parts = self._parse_version(version)[:2]
            t_parts = self._parse_version(target)[:2]
            if v_parts != t_parts:
                return False
            return self._compare_versions(version, target) >= 0
        elif constraint.startswith(">"):
            return self._compare_versions(version, constraint[1:].strip()) > 0
        elif constraint.startswith("<"):
            return self._compare_versions(version, constraint[1:].strip()) < 0
        elif constraint.startswith("=="):
            return self._compare_versions(version, constraint[2:].strip()) == 0
        else:
            return self._compare_versions(version, constraint) == 0

    def add_package(
        self,
        name: str,
        version: str,
        dependencies: list[dict[str, Any]],
        dep_type: str = "required",
    ) -> None:
        self._graph[name][version] = [
            {"name": d["name"], "version": d.get("version", "*"), "type": dep_type}
            for d in dependencies
        ]

    def resolve(self, root: str, version: str) -> list[dict[str, Any]]:
        self._resolved.clear()
        resolution_order: list[dict[str, Any]] = []
        visited: set[str] = set()
        in_stack: set[str] = set()

        def dfs(name: str, version_constraint: str, dep_type: str) -> None:
            resolved_version = self._resolve_version(name, version_constraint)

            if name in in_stack:
                chain = list(visited) + [name]
                raise CircularDependencyError(chain)

            if name in visited:
                if self._resolved.get(name) != resolved_version:
                    raise VersionConflict(name, resolved_version, self._resolved[name])
                return

            in_stack.add(name)
            visited.add(name)
            self._resolved[name] = resolved_version

            resolution_order.append(
                {
                    "name": name,
                    "version": resolved_version,
                    "type": dep_type,
                }
            )

            for dep in self._graph.get(name, {}).get(resolved_version, []):
                dfs(dep["name"], dep["version"], dep["type"])

            in_stack.remove(name)

        dfs(root, version, "root")
        return resolution_order

    def _resolve_version(self, name: str, constraint: str) -> str:
        available = list(self._graph.get(name, {}).keys())
        if not available:
            if constraint == "*" or not constraint:
                return "0.1.0"
            return constraint.lstrip(">=<!^~")

        for ver in sorted(available, key=lambda v: self._parse_version(v), reverse=True):
            if self._satisfies(ver, constraint):
                return ver

        return available[-1] if available else constraint

    def detect_cycles(self) -> list[list[str]]:
        cycles: list[list[str]] = []
        visited: set[str] = set()
        in_stack: set[str] = []
        path: set[str] = set()

        def dfs(node: str) -> None:
            if node in path:
                cycle_start = in_stack.index(node)
                cycles.append(in_stack[cycle_start:] + [node])
                return
            if node in visited:
                return

            visited.add(node)
            in_stack.append(node)
            path.add(node)

            for version_deps in self._graph.get(node, {}).values():
                for dep in version_deps:
                    dfs(dep["name"])

            in_stack.pop()
            path.remove(node)

        for name in self._graph:
            dfs(name)

        return cycles

    def get_dependency_tree(self, name: str, version: str) -> dict[str, Any]:
        tree: dict[str, Any] = {"name": name, "version": version, "dependencies": []}
        visited: set[str] = set()

        def build_tree(pkg_name: str, pkg_version: str, depth: int) -> dict[str, Any]:
            node = {"name": pkg_name, "version": pkg_version, "dependencies": []}
            if pkg_name in visited or depth > 10:
                return node
            visited.add(pkg_name)

            for dep in self._graph.get(pkg_name, {}).get(pkg_version, []):
                child = build_tree(dep["name"], dep["version"], depth + 1)
                node["dependencies"].append(child)

            visited.discard(pkg_name)
            return node

        return build_tree(name, version, 0)

    def visualize_tree(self, name: str, version: str, indent: str = "") -> str:
        tree = self.get_dependency_tree(name, version)
        lines: list[str] = []

        def traverse(node: dict[str, Any], prefix: str, is_last: bool) -> None:
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{node['name']}@{node['version']}")
            deps = node.get("dependencies", [])
            for i, dep in enumerate(deps):
                extension = "    " if is_last else "│   "
                traverse(dep, prefix + extension, i == len(deps) - 1)

        traverse(tree, indent, True)
        return "\n".join(lines)

    def detect_conflicts(self) -> list[dict[str, Any]]:
        conflicts: list[dict[str, Any]] = []
        version_map: dict[str, list[str]] = defaultdict(list)

        for name, versions in self._graph.items():
            for version, deps in versions.items():
                for dep in deps:
                    version_map[dep["name"]].append(dep["version"])

        for dep_name, constraints in version_map.items():
            unique = list(set(constraints))
            if len(unique) > 1:
                conflicts.append(
                    {
                        "package": dep_name,
                        "constraints": unique,
                        "message": f"Multiple version constraints for {dep_name}: {unique}",
                    }
                )

        return conflicts

    def get_install_order(self, name: str, version: str) -> list[str]:
        resolution = self.resolve(name, version)
        return [entry["name"] for entry in resolution]
