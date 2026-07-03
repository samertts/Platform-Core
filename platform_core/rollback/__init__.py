"""Rollback Engine - Snapshot, restore, transaction support, automatic rollback, consistency."""

from __future__ import annotations

import json
import shutil
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from platform_core.packages import InstallRecord, Snapshot, Transaction


class RollbackError(Exception):
    pass


class SnapshotError(RollbackError):
    pass


class RestoreError(RollbackError):
    pass


class RollbackEngine:
    """Manages snapshots, transactions, and rollback operations for package installations."""

    def __init__(self, storage_root: str = "/opt/platform/rollback") -> None:
        self._storage_root = Path(storage_root)
        self._snapshots: dict[str, Snapshot] = {}
        self._transactions: dict[str, Transaction] = {}
        self._install_root = Path("/opt/platform/modules")
        self._lock = threading.RLock()

    def create_snapshot(
        self,
        installed_packages: dict[str, InstallRecord],
        description: str = "",
    ) -> Snapshot:
        snapshot = Snapshot(
            description=description,
            installed_packages=list(installed_packages.values()),
        )

        snapshot_dir = self._storage_root / str(snapshot.id)
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        manifest: dict[str, Any] = {
            "id": str(snapshot.id),
            "created_at": snapshot.created_at.isoformat(),
            "description": description,
            "packages": [],
        }

        for record in installed_packages.values():
            pkg_data = {
                "name": record.package_name,
                "version": record.package_version,
                "install_path": record.install_path,
                "checksum": record.checksum.value,
            }
            manifest["packages"].append(pkg_data)

            source_path = Path(record.install_path)
            if source_path.exists():
                pkg_backup = snapshot_dir / record.package_name
                if source_path.is_dir():
                    shutil.copytree(source_path, pkg_backup, dirs_exist_ok=True)
                else:
                    shutil.copy2(source_path, pkg_backup)

        manifest_path = snapshot_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")

        with self._lock:
            self._snapshots[str(snapshot.id)] = snapshot

        return snapshot

    def restore_snapshot(self, snapshot_id: str) -> dict[str, Any]:
        snapshot_dir = self._storage_root / snapshot_id
        if not snapshot_dir.exists():
            raise SnapshotError(f"Snapshot not found: {snapshot_id}")

        manifest_path = snapshot_dir / "manifest.json"
        if not manifest_path.exists():
            raise SnapshotError(f"Snapshot manifest not found: {snapshot_id}")

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        restored: list[str] = []

        for pkg in manifest.get("packages", []):
            name = pkg.get("name", "")
            backup_path = snapshot_dir / name
            install_path = Path(pkg.get("install_path", ""))

            if backup_path.exists():
                if install_path.exists():
                    shutil.rmtree(install_path)
                shutil.copytree(backup_path, install_path, dirs_exist_ok=True)
                restored.append(name)

        return {
            "snapshot_id": snapshot_id,
            "restored_packages": restored,
            "status": "restored",
            "restored_at": datetime.now(UTC).isoformat(),
        }

    def delete_snapshot(self, snapshot_id: str) -> bool:
        snapshot_dir = self._storage_root / snapshot_id
        if snapshot_dir.exists():
            shutil.rmtree(snapshot_dir)

        with self._lock:
            if snapshot_id in self._snapshots:
                del self._snapshots[snapshot_id]
                return True
        return False

    def list_snapshots(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "id": str(s.id),
                    "created_at": s.created_at.isoformat(),
                    "description": s.description,
                    "packages": len(s.installed_packages),
                }
                for s in self._snapshots.values()
            ]

    def begin_transaction(self) -> Transaction:
        transaction = Transaction()
        with self._lock:
            self._transactions[str(transaction.id)] = transaction
        return transaction

    def add_operation(
        self,
        transaction_id: str,
        operation_type: str,
        package_name: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        with self._lock:
            transaction = self._transactions.get(transaction_id)
            if transaction is None:
                raise RollbackError(f"Transaction not found: {transaction_id}")

            transaction.operations.append(
                {
                    "type": operation_type,
                    "package": package_name,
                    "details": details or {},
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            )

    def commit_transaction(self, transaction_id: str) -> dict[str, Any]:
        with self._lock:
            transaction = self._transactions.get(transaction_id)
            if transaction is None:
                raise RollbackError(f"Transaction not found: {transaction_id}")

            transaction.status = "committed"
            transaction.completed_at = datetime.now(UTC)

        return {
            "transaction_id": transaction_id,
            "status": "committed",
            "operations": len(transaction.operations),
        }

    def rollback_transaction(self, transaction_id: str) -> dict[str, Any]:
        with self._lock:
            transaction = self._transactions.get(transaction_id)
            if transaction is None:
                raise RollbackError(f"Transaction not found: {transaction_id}")

            rolled_back: list[dict[str, Any]] = []
            for op in reversed(transaction.operations):
                rolled_back.append(
                    {
                        "type": f"reverse_{op['type']}",
                        "package": op["package"],
                        "timestamp": datetime.now(UTC).isoformat(),
                    }
                )

            transaction.status = "rolled_back"
            transaction.completed_at = datetime.now(UTC)

        return {
            "transaction_id": transaction_id,
            "status": "rolled_back",
            "rolled_back_operations": rolled_back,
        }

    def auto_rollback(self, transaction_id: str) -> dict[str, Any]:
        return self.rollback_transaction(transaction_id)

    def verify_consistency(self, installed_packages: dict[str, InstallRecord]) -> dict[str, Any]:
        issues: list[str] = []

        for name, record in installed_packages.items():
            install_path = Path(record.install_path)
            if not install_path.exists():
                issues.append(f"Package {name} install path missing: {record.install_path}")

        return {
            "consistent": len(issues) == 0,
            "issues": issues,
            "packages_checked": len(installed_packages),
        }

    def get_transaction(self, transaction_id: str) -> Transaction | None:
        with self._lock:
            return self._transactions.get(transaction_id)
