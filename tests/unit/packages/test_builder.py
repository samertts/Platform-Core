"""Unit tests for Package Builder."""

import os
from pathlib import Path

import pytest

from platform_core.builder import BuildError, PackageBuilder


class TestPackageBuilder:
    def test_init(self) -> None:
        builder = PackageBuilder()
        assert builder is not None

    def test_generate_manifest(self) -> None:
        builder = PackageBuilder()
        manifest = builder.generate_manifest(
            name="test-pkg",
            version="1.0.0",
            description="Test package",
            publisher="test-pub",
        )
        assert manifest.package.name == "test-pkg"
        assert manifest.package.version == "1.0.0"
        assert manifest.package.publisher == "test-pub"

    def test_generate_manifest_with_deps(self) -> None:
        builder = PackageBuilder()
        manifest = builder.generate_manifest(
            name="test",
            version="1.0.0",
            dependencies=[{"name": "dep1", "version": ">=1.0.0"}],
        )
        assert len(manifest.dependencies.required) == 1

    def test_generate_sbom(self) -> None:
        builder = PackageBuilder()
        manifest = builder.generate_manifest(name="test", version="1.0.0")
        sbom = builder.generate_sbom(manifest, ["main.py", "utils.py"])
        assert sbom["sbom_version"] == "1.0.0"
        assert len(sbom["components"]) == 2

    def test_compute_checksum_sha256(self) -> None:
        builder = PackageBuilder()
        checksum = builder.compute_checksum(b"test data", "sha256")
        assert len(checksum) == 64

    def test_compute_checksum_sha512(self) -> None:
        builder = PackageBuilder()
        checksum = builder.compute_checksum(b"test data", "sha512")
        assert len(checksum) == 128

    def test_compute_checksum_invalid(self) -> None:
        builder = PackageBuilder()
        with pytest.raises(ValueError, match="Unsupported algorithm"):
            builder.compute_checksum(b"test", "md5")

    def test_sign_package(self) -> None:
        builder = PackageBuilder()
        sig = builder.sign_package(b"test data", "my-key")
        assert sig.signature is not None
        assert sig.signer == "my-key"

    def test_sign_package_default(self) -> None:
        builder = PackageBuilder()
        sig = builder.sign_package(b"test data")
        assert sig.signer == "platform-core"

    def test_build_package(self, tmp_path: Path) -> None:
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "main.py").write_text("print('hello')")
        (source_dir / "utils.py").write_text("# utils")

        output_dir = tmp_path / "output"
        builder = PackageBuilder(output_dir=str(output_dir))
        manifest = builder.generate_manifest(name="test", version="1.0.0")
        result = builder.build_package(str(source_dir), manifest, sign=False)
        assert os.path.exists(result)

    def test_build_package_signed(self, tmp_path: Path) -> None:
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "main.py").write_text("print('hello')")

        output_dir = tmp_path / "output"
        builder = PackageBuilder(output_dir=str(output_dir))
        manifest = builder.generate_manifest(name="test", version="1.0.0")
        result = builder.build_package(str(source_dir), manifest, sign=True, private_key="test-key")
        assert os.path.exists(result)
        assert os.path.exists(result + ".sig")

    def test_build_package_source_not_found(self, tmp_path: Path) -> None:
        builder = PackageBuilder(output_dir=str(tmp_path / "output"))
        manifest = builder.generate_manifest(name="test", version="1.0.0")
        with pytest.raises(BuildError, match="Source directory not found"):
            builder.build_package("/nonexistent", manifest)

    def test_build_package_creates_checksum(self, tmp_path: Path) -> None:
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "main.py").write_text("x = 1")

        output_dir = tmp_path / "output"
        builder = PackageBuilder(output_dir=str(output_dir))
        manifest = builder.generate_manifest(name="test", version="1.0.0")
        result = builder.build_package(str(source_dir), manifest, sign=False)
        assert os.path.exists(result + ".sha256")

    def test_get_build_log(self) -> None:
        builder = PackageBuilder()
        log = builder.get_build_log()
        assert isinstance(log, list)

    def test_generate_manifest_defaults(self) -> None:
        builder = PackageBuilder()
        manifest = builder.generate_manifest(name="test", version="1.0.0")
        assert manifest.package.license == "proprietary"
        assert manifest.compatibility.platform_core == ">=1.0.0"
