"""Unit tests for Module Installer."""

from pathlib import Path

import pytest

from platform_core.installer import ModuleInstaller, ValidationError
from platform_core.packages import PackageDependencies, PackageIdentity, PackageManifest


class TestModuleInstaller:
    def test_init(self) -> None:
        installer = ModuleInstaller()
        assert installer is not None

    def test_pre_install_validate_missing_path(self) -> None:
        installer = ModuleInstaller()
        manifest = PackageManifest(package=PackageIdentity(name="test", version="1.0.0"))
        errors = installer.pre_install_validate("/nonexistent", manifest)
        assert len(errors) > 0

    def test_pre_install_validate_empty_name(self) -> None:
        installer = ModuleInstaller()
        manifest = PackageManifest(package=PackageIdentity(name="", version="1.0.0"))
        errors = installer.pre_install_validate("/tmp", manifest)
        assert len(errors) > 0

    def test_install_dependencies(self) -> None:
        installer = ModuleInstaller()
        manifest = PackageManifest(package=PackageIdentity(name="test", version="1.0.0"))
        results = installer.install_dependencies(manifest)
        assert isinstance(results, list)

    def test_install(self, tmp_path: Path) -> None:
        installer = ModuleInstaller(install_root=str(tmp_path))
        pkg_dir = tmp_path / "source"
        pkg_dir.mkdir()
        (pkg_dir / "main.py").write_text("x = 1")
        manifest = PackageManifest(package=PackageIdentity(name="test", version="1.0.0"))
        record = installer.install(str(pkg_dir), manifest)
        assert record.package_name == "test"
        assert record.status.value == "completed"

    def test_install_dry_run(self, tmp_path: Path) -> None:
        installer = ModuleInstaller(install_root=str(tmp_path))
        pkg_dir = tmp_path / "source"
        pkg_dir.mkdir()
        manifest = PackageManifest(package=PackageIdentity(name="test", version="1.0.0"))
        record = installer.install(str(pkg_dir), manifest, dry_run=True)
        assert record.status.value == "pending"

    def test_install_validation_error(self) -> None:
        installer = ModuleInstaller()
        manifest = PackageManifest(package=PackageIdentity(name="", version="1.0.0"))
        with pytest.raises(ValidationError):
            installer.install("/nonexistent", manifest)

    def test_uninstall(self, tmp_path: Path) -> None:
        installer = ModuleInstaller(install_root=str(tmp_path))
        pkg_dir = tmp_path / "source"
        pkg_dir.mkdir()
        manifest = PackageManifest(package=PackageIdentity(name="test", version="1.0.0"))
        installer.install(str(pkg_dir), manifest)
        assert installer.uninstall("test")
        assert not installer.uninstall("nonexistent")

    def test_verify_installation(self, tmp_path: Path) -> None:
        installer = ModuleInstaller(install_root=str(tmp_path))
        pkg_dir = tmp_path / "source"
        pkg_dir.mkdir()
        manifest = PackageManifest(package=PackageIdentity(name="test", version="1.0.0"))
        installer.install(str(pkg_dir), manifest)
        result = installer.verify_installation("test")
        assert result["installed"] is True
        assert result["version"] == "1.0.0"

    def test_verify_installation_not_found(self) -> None:
        installer = ModuleInstaller()
        result = installer.verify_installation("nonexistent")
        assert result["installed"] is False

    def test_get_installed_packages(self, tmp_path: Path) -> None:
        installer = ModuleInstaller(install_root=str(tmp_path))
        pkg_dir = tmp_path / "source"
        pkg_dir.mkdir()
        manifest = PackageManifest(package=PackageIdentity(name="test", version="1.0.0"))
        installer.install(str(pkg_dir), manifest)
        installed = installer.get_installed_packages()
        assert len(installed) == 1

    def test_get_install_log(self, tmp_path: Path) -> None:
        installer = ModuleInstaller(install_root=str(tmp_path))
        pkg_dir = tmp_path / "source"
        pkg_dir.mkdir()
        manifest = PackageManifest(package=PackageIdentity(name="test", version="1.0.0"))
        installer.install(str(pkg_dir), manifest)
        log = installer.get_install_log()
        assert len(log) > 0

    def test_repair(self, tmp_path: Path) -> None:
        installer = ModuleInstaller(install_root=str(tmp_path))
        pkg_dir = tmp_path / "source"
        pkg_dir.mkdir()
        manifest = PackageManifest(package=PackageIdentity(name="test", version="1.0.0"))
        installer.install(str(pkg_dir), manifest)
        result = installer.repair("test")
        assert result["repaired"] is True

    def test_repair_not_found(self) -> None:
        installer = ModuleInstaller()
        result = installer.repair("nonexistent")
        assert result["repaired"] is False

    def test_install_with_deps(self, tmp_path: Path) -> None:
        installer = ModuleInstaller(install_root=str(tmp_path))
        pkg_dir = tmp_path / "source"
        pkg_dir.mkdir()
        (pkg_dir / "main.py").write_text("x = 1")
        manifest = PackageManifest(
            package=PackageIdentity(name="test", version="1.0.0"),
            dependencies=PackageDependencies(required=[{"name": "dep1", "version": ">=1.0.0"}]),
        )
        record = installer.install(str(pkg_dir), manifest)
        assert record.package_name == "test"
