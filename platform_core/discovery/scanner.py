"""Scanner - Filesystem-based repository structure scanning."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from platform_core.discovery.types import ScanResult, ScanStatus, ScanType


class ScanError(Exception):
    pass


class Scanner:
    """Scans repository filesystem structure and collects metadata."""

    DEFAULT_EXCLUDES = {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        ".next",
        ".nuxt",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "eggs",
        "*.egg-info",
    }

    DEFAULT_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    DEFAULT_MAX_FILES = 50000

    def __init__(
        self,
        excludes: set[str] | None = None,
        max_file_size: int = DEFAULT_MAX_FILE_SIZE,
        max_files: int = DEFAULT_MAX_FILES,
    ) -> None:
        self._excludes = excludes or self.DEFAULT_EXCLUDES.copy()
        self._max_file_size = max_file_size
        self._max_files = max_files

    def scan(
        self,
        root_path: str,
        scan_type: ScanType = ScanType.FULL,
        repository: str = "",
    ) -> ScanResult:
        root = Path(root_path)
        if not root.exists():
            raise ScanError(f"Path does not exist: {root_path}")
        if not root.is_dir():
            raise ScanError(f"Path is not a directory: {root_path}")

        result = ScanResult(
            repository=repository or root.name,
            scan_type=scan_type,
            status=ScanStatus.RUNNING,
            started_at=datetime.now(UTC),
            root_path=str(root.resolve()),
        )

        try:
            files = self._collect_files(root)
            result.total_files = len(files)
            result.files_scanned = len(files)
            result.status = ScanStatus.SUCCESS
        except Exception as e:
            result.status = ScanStatus.FAILED
            result.errors.append(str(e))

        result.completed_at = datetime.now(UTC)
        result.duration_seconds = (result.completed_at - result.started_at).total_seconds()

        return result

    def _collect_files(self, root: Path) -> list[dict[str, Any]]:
        files: list[dict[str, Any]] = []
        count = 0

        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not self._should_exclude(d)]

            for filename in filenames:
                if count >= self._max_files:
                    return files

                if self._should_exclude(filename):
                    continue

                filepath = Path(dirpath) / filename
                try:
                    stat = filepath.stat()
                    if stat.st_size > self._max_file_size:
                        continue

                    rel_path = str(filepath.relative_to(root))
                    files.append(
                        {
                            "path": rel_path,
                            "name": filename,
                            "extension": filepath.suffix.lower(),
                            "size": stat.st_size,
                            "modified_at": datetime.fromtimestamp(
                                stat.st_mtime, tz=UTC
                            ).isoformat(),
                        }
                    )
                    count += 1
                except (PermissionError, OSError):
                    continue

        return files

    def _should_exclude(self, name: str) -> bool:
        for pattern in self._excludes:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True
        return False

    def get_file_tree(self, root_path: str, max_depth: int = 5) -> dict[str, Any]:
        root = Path(root_path)
        if not root.exists():
            return {}

        return self._build_tree(root, root, max_depth, 0)

    def _build_tree(self, root: Path, current: Path, max_depth: int, depth: int) -> dict[str, Any]:
        node: dict[str, Any] = {
            "name": current.name,
            "type": "dir" if current.is_dir() else "file",
        }

        if current.is_dir():
            if depth >= max_depth:
                node["truncated"] = True
                return node

            children = []
            try:
                entries = sorted(current.iterdir(), key=lambda p: (p.is_file(), p.name))
                for entry in entries:
                    if self._should_exclude(entry.name):
                        continue
                    child = self._build_tree(root, entry, max_depth, depth + 1)
                    children.append(child)
            except PermissionError:
                pass

            node["children"] = children

        return node

    def get_repository_metadata(self, root_path: str) -> dict[str, Any]:
        root = Path(root_path)
        metadata: dict[str, Any] = {
            "name": root.name,
            "path": str(root.resolve()),
            "has_readme": False,
            "has_license": False,
            "has_gitignore": False,
            "has_manifest": False,
            "entry_points": [],
        }

        for item in root.iterdir():
            if item.name.lower().startswith("readme"):
                metadata["has_readme"] = True
            elif item.name.lower() == "license":
                metadata["has_license"] = True
            elif item.name.lower() == ".gitignore":
                metadata["has_gitignore"] = True
            elif item.name.lower() in (
                "platform-manifest.yaml",
                "platform-manifest.json",
            ):
                metadata["has_manifest"] = True
            elif item.name in (
                "main.py",
                "app.py",
                "index.ts",
                "index.js",
                "main.go",
                "cmd",
            ):
                metadata["entry_points"].append(item.name)

        return metadata
