"""Unit tests for Compatibility Engine."""

import pytest
from platform_core.packages.compatibility import CompatibilityEngine


class TestCompatibilityEngine:
    def test_init(self) -> None:
        engine = CompatibilityEngine()
        assert engine._platform_version == "1.0.0"

    def test_init_custom_version(self) -> None:
        engine = CompatibilityEngine(platform_version="2.0.0")
        assert engine._platform_version == "2.0.0"

    def test_check_runtime_compatibility_python(self) -> None:
        engine = CompatibilityEngine()
        result = engine.check_runtime_compatibility("python>=3.10", "3.11")
        assert result["compatible"] is True
        assert result["runtime"] == "python"

    def test_check_runtime_compatibility_exact(self) -> None:
        engine = CompatibilityEngine()
        result = engine.check_runtime_compatibility("python>=3.10", "3.9")
        assert result["compatible"] is False

    def test_check_runtime_compatibility_unsupported(self) -> None:
        engine = CompatibilityEngine()
        result = engine.check_runtime_compatibility("java8", "8.0")
        assert result["compatible"] is False
        assert "Unsupported" in result["error"]

    def test_check_runtime_compatibility_no_constraint(self) -> None:
        engine = CompatibilityEngine()
        result = engine.check_runtime_compatibility("python", "3.11")
        assert result["compatible"] is True

    def test_check_sdk_compatibility(self) -> None:
        engine = CompatibilityEngine()
        result = engine.check_sdk_compatibility(">=1.0.0", "1.2.0")
        assert result["compatible"] is True

    def test_check_sdk_compatibility_incompatible(self) -> None:
        engine = CompatibilityEngine()
        result = engine.check_sdk_compatibility(">=2.0.0", "1.0.0")
        assert result["compatible"] is False

    def test_check_platform_compatibility(self) -> None:
        engine = CompatibilityEngine(platform_version="1.0.0")
        result = engine.check_platform_compatibility(">=1.0.0")
        assert result["compatible"] is True

    def test_check_platform_compatibility_incompatible(self) -> None:
        engine = CompatibilityEngine(platform_version="0.9.0")
        result = engine.check_platform_compatibility(">=1.0.0")
        assert result["compatible"] is False

    def test_check_manifest_compatibility(self) -> None:
        engine = CompatibilityEngine()
        manifest = {
            "compatibility": {"platform_core": ">=1.0.0"},
            "runtime": {"language": "python", "version": "3.11"},
        }
        result = engine.check_manifest_compatibility(manifest)
        assert result["compatible"] is True

    def test_check_manifest_compatibility_bad_platform(self) -> None:
        engine = CompatibilityEngine(platform_version="0.5.0")
        manifest = {"compatibility": {"platform_core": ">=1.0.0"}}
        result = engine.check_manifest_compatibility(manifest)
        assert result["compatible"] is False

    def test_check_version_compatibility(self) -> None:
        engine = CompatibilityEngine(platform_version="1.5.0")
        result = engine.check_version_compatibility("1.0.0", ">=1.0.0")
        assert result["compatible"] is True

    def test_check_version_compatibility_too_old(self) -> None:
        engine = CompatibilityEngine(platform_version="0.5.0")
        result = engine.check_version_compatibility("1.0.0", ">=1.0.0")
        assert result["compatible"] is False

    def test_check_migration_compatibility(self) -> None:
        engine = CompatibilityEngine()
        result = engine.check_migration_compatibility("1.0.0", "2.0.0")
        assert result["compatible"] is True

    def test_check_migration_compatibility_same_version(self) -> None:
        engine = CompatibilityEngine()
        result = engine.check_migration_compatibility("1.0.0", "1.0.0")
        assert result["compatible"] is False

    def test_check_migration_compatibility_bad_path(self) -> None:
        engine = CompatibilityEngine()
        result = engine.check_migration_compatibility(
            "1.0.0", "3.0.0", migration_path=["1.0.0", "3.0.0", "2.0.0"]
        )
        assert result["compatible"] is False

    def test_full_compatibility_check(self) -> None:
        engine = CompatibilityEngine()
        manifest = {
            "compatibility": {"platform_core": ">=1.0.0"},
            "runtime": {"language": "python", "version": "3.11"},
        }
        result = engine.full_compatibility_check(manifest)
        assert result["overall_compatible"] is True
        assert "manifest" in result
        assert "platform" in result
        assert "runtime" in result

    def test_satisfies_exact(self) -> None:
        engine = CompatibilityEngine()
        assert engine._satisfies("1.0.0", "==1.0.0")
        assert not engine._satisfies("1.0.1", "==1.0.0")

    def test_satisfies_not_equal(self) -> None:
        engine = CompatibilityEngine()
        assert engine._satisfies("2.0.0", "!=1.0.0")

    def test_satisfies_caret(self) -> None:
        engine = CompatibilityEngine()
        assert engine._satisfies("1.2.0", "^1.0.0")
        assert not engine._satisfies("2.0.0", "^1.0.0")

    def test_satisfies_less_than(self) -> None:
        engine = CompatibilityEngine()
        assert engine._satisfies("0.9.0", "<1.0.0")
        assert not engine._satisfies("1.0.0", "<1.0.0")

    def test_satisfies_less_than_equal(self) -> None:
        engine = CompatibilityEngine()
        assert engine._satisfies("1.0.0", "<=1.0.0")
        assert not engine._satisfies("1.0.1", "<=1.0.0")

    def test_satisfies_greater_than(self) -> None:
        engine = CompatibilityEngine()
        assert engine._satisfies("1.0.1", ">1.0.0")
        assert not engine._satisfies("1.0.0", ">1.0.0")

    def test_compare_versions(self) -> None:
        engine = CompatibilityEngine()
        assert engine._compare_versions("1.0.0", "2.0.0") < 0
        assert engine._compare_versions("2.0.0", "1.0.0") > 0
        assert engine._compare_versions("1.0.0", "1.0.0") == 0

    def test_parse_version(self) -> None:
        engine = CompatibilityEngine()
        result = engine._parse_version("1.2.3")
        assert result == (1, 2, 3)
