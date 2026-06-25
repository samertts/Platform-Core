"""Unit tests for Update Manager."""

import pytest
from platform_core.updater import UpdateManager, UpdateError
from platform_core.packages import InstallRecord, InstallStatus, PackageManifest


class TestUpdateManager:
    def test_init(self) -> None:
        updater = UpdateManager()
        assert updater is not None

    def test_register_installed(self) -> None:
        updater = UpdateManager()
        record = InstallRecord(package_name="pkg", package_version="1.0.0")
        updater.register_installed(record)
        assert "pkg" in updater._installed

    def test_check_updates(self) -> None:
        updater = UpdateManager()
        record = InstallRecord(package_name="pkg", package_version="1.0.0")
        updater.register_installed(record)
        updates = updater.check_updates({"pkg": ["1.0.0", "2.0.0", "3.0.0"]})
        assert len(updates) == 2  # 2.0.0 and 3.0.0
        assert updates[0]["available_version"] == "2.0.0"

    def test_check_updates_no_updates(self) -> None:
        updater = UpdateManager()
        record = InstallRecord(package_name="pkg", package_version="2.0.0")
        updater.register_installed(record)
        updates = updater.check_updates({"pkg": ["1.0.0", "2.0.0"]})
        assert len(updates) == 0

    def test_download_update(self) -> None:
        updater = UpdateManager()
        result = updater.download_update("pkg", "2.0.0")
        assert result["status"] == "downloaded"

    def test_validate_update(self) -> None:
        updater = UpdateManager()
        manifest = PackageManifest()
        manifest.package.name = "pkg"
        manifest.package.version = "2.0.0"
        result = updater.validate_update("pkg", "2.0.0", manifest)
        assert result["valid"] is True

    def test_stage_update(self) -> None:
        updater = UpdateManager()
        result = updater.stage_update("pkg", "2.0.0")
        assert result["status"] == "staged"

    def test_apply_update(self) -> None:
        updater = UpdateManager()
        updater.stage_update("pkg", "2.0.0")
        result = updater.apply_update("pkg", "2.0.0")
        assert result["status"] == "applied"

    def test_apply_update_not_staged(self) -> None:
        updater = UpdateManager()
        with pytest.raises(UpdateError):
            updater.apply_update("pkg", "2.0.0")

    def test_rollback_update(self) -> None:
        updater = UpdateManager()
        updater.stage_update("pkg", "2.0.0")
        result = updater.rollback_update("pkg")
        assert result["status"] == "rolled_back"

    def test_rollback_update_nothing(self) -> None:
        updater = UpdateManager()
        result = updater.rollback_update("pkg")
        assert result["status"] == "rolled_back"
        assert result["action"] == "nothing_to_rollback"

    def test_get_available_updates(self) -> None:
        updater = UpdateManager()
        updater.stage_update("a", "2.0.0")
        updater.stage_update("b", "3.0.0")
        updates = updater.get_available_updates()
        assert len(updates) == 2

    def test_get_update_log(self) -> None:
        updater = UpdateManager()
        updater.stage_update("pkg", "2.0.0")
        log = updater.get_update_log()
        assert len(log) > 0
