"""Compatibility Engine - Runtime, SDK, policy, manifest, version, migration compatibility."""

from __future__ import annotations

import re
from typing import Any


class CompatibilityError(Exception):
    pass


class CompatibilityEngine:
    """Validates compatibility across runtime, SDK, policy, manifest, and version dimensions."""

    def __init__(self, platform_version: str = "1.0.0") -> None:
        self._platform_version = platform_version
        self._compatibility_cache: dict[str, bool] = {}

    def _parse_version(self, version: str) -> tuple[int, ...]:
        parts = re.findall(r"\d+", version)
        return tuple(int(p) for p in parts)

    def _compare_versions(self, v1: str, v2: str) -> int:
        parts1 = self._parse_version(v1)
        parts2 = self._parse_version(v2)
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

    def _satisfies(self, version: str, constraint: str) -> bool:
        constraint = constraint.strip()
        if not constraint or constraint == "*":
            return True

        if constraint.startswith(">="):
            return self._compare_versions(version, constraint[2:].strip()) >= 0
        elif constraint.startswith("<="):
            return self._compare_versions(version, constraint[2:].strip()) <= 0
        elif constraint.startswith("!="):
            return self._compare_versions(version, constraint[2:].strip()) != 0
        elif constraint.startswith("^"):
            target = constraint[1:].strip()
            v_parts = self._parse_version(version)
            t_parts = self._parse_version(target)
            if v_parts[0] != t_parts[0]:
                return False
            return self._compare_versions(version, target) >= 0
        elif constraint.startswith("~"):
            target = constraint[1:].strip()
            v_parts = self._parse_version(version)[:2]
            t_parts = self._parse_version(target)[:2]
            return v_parts == t_parts
        elif constraint.startswith(">"):
            return self._compare_versions(version, constraint[1:].strip()) > 0
        elif constraint.startswith("<"):
            return self._compare_versions(version, constraint[1:].strip()) < 0
        elif constraint.startswith("=="):
            return self._compare_versions(version, constraint[2:].strip()) == 0
        else:
            return self._compare_versions(version, constraint) == 0

    def check_runtime_compatibility(
        self,
        package_runtime: str,
        package_version: str,
    ) -> dict[str, Any]:
        match = re.match(r"([a-zA-Z]+)(.*)", package_runtime)
        if not match:
            return {"compatible": False, "error": f"Invalid runtime: {package_runtime}"}

        lang = match.group(1).lower()
        version_constraint = match.group(2).strip()

        if lang != "python":
            return {"compatible": False, "error": f"Unsupported runtime: {lang}"}

        if version_constraint:
            compatible = self._satisfies(package_version, version_constraint)
            return {
                "compatible": compatible,
                "runtime": lang,
                "constraint": version_constraint,
                "actual": package_version,
            }

        return {"compatible": True, "runtime": lang}

    def check_sdk_compatibility(
        self,
        package_sdk_version: str,
        platform_sdk_version: str,
    ) -> dict[str, Any]:
        compatible = self._satisfies(platform_sdk_version, package_sdk_version)
        return {
            "compatible": compatible,
            "required": package_sdk_version,
            "available": platform_sdk_version,
        }

    def check_platform_compatibility(
        self,
        platform_constraint: str,
    ) -> dict[str, Any]:
        compatible = self._satisfies(self._platform_version, platform_constraint)
        return {
            "compatible": compatible,
            "required": platform_constraint,
            "actual": self._platform_version,
        }

    def check_manifest_compatibility(
        self,
        manifest: dict[str, Any],
    ) -> dict[str, Any]:
        issues: list[str] = []
        warnings: list[str] = []

        compatibility = manifest.get("compatibility", {})
        if "platform_core" in compatibility:
            result = self.check_platform_compatibility(compatibility["platform_core"])
            if not result["compatible"]:
                issues.append(
                    f"Platform version incompatible: requires {result['required']}, "
                    f"have {result['actual']}"
                )

        runtime = manifest.get("runtime", {})
        if "language" in runtime and "version" in runtime:
            runtime_str = f"{runtime['language']}{runtime['version']}"
            result = self.check_runtime_compatibility(runtime_str, runtime.get("version", "3.11"))
            if not result["compatible"]:
                issues.append(f"Runtime incompatible: {result.get('error', 'unknown')}")

        dependencies = manifest.get("dependencies", {})
        for dep in dependencies.get("required", []):
            if "version" in dep and "name" in dep:
                if not self._satisfies("1.0.0", dep["version"]):
                    warnings.append(f"Dependency {dep['name']} may need version check")

        return {
            "compatible": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
        }

    def check_version_compatibility(
        self,
        package_version: str,
        min_platform_version: str,
        max_platform_version: str = "",
    ) -> dict[str, Any]:
        issues: list[str] = []

        if min_platform_version:
            if not self._satisfies(self._platform_version, min_platform_version):
                issues.append(
                    f"Platform version too old: {self._platform_version} < {min_platform_version}"
                )

        if max_platform_version:
            if self._compare_versions(self._platform_version, max_platform_version) > 0:
                issues.append(
                    f"Platform version too new: {self._platform_version} > {max_platform_version}"
                )

        return {
            "compatible": len(issues) == 0,
            "issues": issues,
            "platform_version": self._platform_version,
        }

    def check_migration_compatibility(
        self,
        from_version: str,
        to_version: str,
        migration_path: list[str] | None = None,
    ) -> dict[str, Any]:
        issues: list[str] = []

        if self._compare_versions(from_version, to_version) >= 0:
            issues.append("Migration must be to a newer version")

        if migration_path:
            for i, step in enumerate(migration_path):
                if i > 0:
                    prev = migration_path[i - 1]
                    if self._compare_versions(prev, step) >= 0:
                        issues.append(
                            f"Migration path must be monotonically increasing: {prev} -> {step}"
                        )

        return {
            "compatible": len(issues) == 0,
            "issues": issues,
            "from_version": from_version,
            "to_version": to_version,
        }

    def full_compatibility_check(self, manifest: dict[str, Any]) -> dict[str, Any]:
        results: dict[str, Any] = {
            "manifest": self.check_manifest_compatibility(manifest),
            "platform": {"compatible": True},
            "runtime": {"compatible": True},
            "sdk": {"compatible": True},
            "overall_compatible": True,
        }

        compatibility = manifest.get("compatibility", {})
        if "platform_core" in compatibility:
            results["platform"] = self.check_platform_compatibility(compatibility["platform_core"])

        runtime = manifest.get("runtime", {})
        if "language" in runtime:
            runtime_str = f"{runtime['language']}{runtime.get('version', '')}"
            results["runtime"] = self.check_runtime_compatibility(
                runtime_str, runtime.get("version", "3.11")
            )

        if "sdk_version" in compatibility:
            results["sdk"] = self.check_sdk_compatibility(compatibility["sdk_version"], "1.0.0")

        results["overall_compatible"] = all(
            r.get("compatible", True) for r in results.values() if isinstance(r, dict)
        )

        return results
