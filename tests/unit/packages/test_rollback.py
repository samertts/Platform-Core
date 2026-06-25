"""Unit tests for Rollback Engine."""

import pytest
from platform_core.rollback import RollbackEngine, RollbackError, SnapshotError
from platform_core.packages import InstallRecord, InstallStatus


def _make_record(tmp_path, name="pkg", version="1.0.0"):
    pkg_dir = tmp_path / name
    pkg_dir.mkdir(exist_ok=True)
    (pkg_dir / "main.py").write_text(f"# {name}")
    return InstallRecord(
        package_name=name,
        package_version=version,
        install_path=str(pkg_dir),
    )


class TestRollbackEngine:
    def test_init(self) -> None:
        engine = RollbackEngine(storage_root="/tmp/test_rollback")
        assert engine is not None

    def test_create_snapshot(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        packages = {"pkg": _make_record(tmp_path)}
        snap = engine.create_snapshot(packages, "test snapshot")
        assert snap.description == "test snapshot"
        assert len(snap.installed_packages) == 1

    def test_list_snapshots(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        packages = {"a": _make_record(tmp_path, "a")}
        engine.create_snapshot(packages)
        snaps = engine.list_snapshots()
        assert len(snaps) == 1
        assert snaps[0]["packages"] == 1

    def test_delete_snapshot(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        packages = {"pkg": _make_record(tmp_path)}
        snap = engine.create_snapshot(packages)
        assert engine.delete_snapshot(str(snap.id))
        assert engine.list_snapshots() == []

    def test_delete_nonexistent_snapshot(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        assert not engine.delete_snapshot("nonexistent")

    def test_begin_transaction(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        txn = engine.begin_transaction()
        assert txn.status == "pending"

    def test_add_operation(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        txn = engine.begin_transaction()
        engine.add_operation(str(txn.id), "install", "pkg")
        assert len(txn.operations) == 1

    def test_add_operation_nonexistent(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        with pytest.raises(RollbackError):
            engine.add_operation("nonexistent", "install", "pkg")

    def test_commit_transaction(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        txn = engine.begin_transaction()
        engine.add_operation(str(txn.id), "install", "pkg")
        result = engine.commit_transaction(str(txn.id))
        assert result["status"] == "committed"

    def test_rollback_transaction(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        txn = engine.begin_transaction()
        engine.add_operation(str(txn.id), "install", "pkg")
        engine.add_operation(str(txn.id), "update", "pkg2")
        result = engine.rollback_transaction(str(txn.id))
        assert result["status"] == "rolled_back"
        assert len(result["rolled_back_operations"]) == 2

    def test_rollback_transaction_nonexistent(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        with pytest.raises(RollbackError):
            engine.rollback_transaction("nonexistent")

    def test_auto_rollback(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        txn = engine.begin_transaction()
        engine.add_operation(str(txn.id), "install", "pkg")
        result = engine.auto_rollback(str(txn.id))
        assert result["status"] == "rolled_back"

    def test_verify_consistency(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        packages = {
            "pkg": InstallRecord(
                package_name="pkg",
                package_version="1.0.0",
                install_path="/nonexistent",
            )
        }
        result = engine.verify_consistency(packages)
        assert result["consistent"] is False
        assert len(result["issues"]) == 1

    def test_verify_consistency_empty(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        result = engine.verify_consistency({})
        assert result["consistent"] is True

    def test_get_transaction(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        txn = engine.begin_transaction()
        retrieved = engine.get_transaction(str(txn.id))
        assert retrieved is not None
        assert str(retrieved.id) == str(txn.id)

    def test_get_transaction_nonexistent(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        assert engine.get_transaction("nonexistent") is None

    def test_multiple_transactions(self, tmp_path) -> None:
        engine = RollbackEngine(storage_root=str(tmp_path / "rollback"))
        t1 = engine.begin_transaction()
        t2 = engine.begin_transaction()
        engine.add_operation(str(t1.id), "install", "a")
        engine.add_operation(str(t2.id), "install", "b")
        result1 = engine.commit_transaction(str(t1.id))
        result2 = engine.commit_transaction(str(t2.id))
        assert result1["status"] == "committed"
        assert result2["status"] == "committed"
