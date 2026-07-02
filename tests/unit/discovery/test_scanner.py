"""Unit tests for Scanner."""

import pytest

from platform_core.discovery.scanner import ScanError, Scanner
from platform_core.discovery.types import ScanStatus, ScanType


class TestScanner:
    def test_init(self) -> None:
        scanner = Scanner()
        assert scanner is not None

    def test_scan_nonexistent_path(self) -> None:
        scanner = Scanner()
        with pytest.raises(ScanError, match="does not exist"):
            scanner.scan("/nonexistent/path")

    def test_scan_file_not_dir(self, tmp_path) -> None:
        f = tmp_path / "file.txt"
        f.write_text("hello")
        scanner = Scanner()
        with pytest.raises(ScanError, match="not a directory"):
            scanner.scan(str(f))

    def test_scan_empty_directory(self, tmp_path) -> None:
        scanner = Scanner()
        result = scanner.scan(str(tmp_path), repository="empty")
        assert result.status == ScanStatus.SUCCESS
        assert result.repository == "empty"
        assert result.files_scanned == 0

    def test_scan_with_files(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("print('hello')")
        (tmp_path / "utils.py").write_text("# utils")
        (tmp_path / "README.md").write_text("# Test")
        scanner = Scanner()
        result = scanner.scan(str(tmp_path), repository="test-repo")
        assert result.status == ScanStatus.SUCCESS
        assert result.files_scanned == 3

    def test_scan_excludes_git(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("git config")
        scanner = Scanner()
        result = scanner.scan(str(tmp_path))
        assert result.files_scanned == 1

    def test_scan_excludes_node_modules(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        nm = tmp_path / "node_modules"
        nm.mkdir()
        (nm / "pkg.js").write_text("module.exports = {}")
        scanner = Scanner()
        result = scanner.scan(str(tmp_path))
        assert result.files_scanned == 1

    def test_scan_respects_max_files(self, tmp_path) -> None:
        for i in range(10):
            (tmp_path / f"file_{i}.py").write_text(f"x = {i}")
        scanner = Scanner(max_files=5)
        result = scanner.scan(str(tmp_path))
        assert result.files_scanned == 5

    def test_scan_excludes_large_files(self, tmp_path) -> None:
        (tmp_path / "small.py").write_text("x = 1")
        (tmp_path / "large.bin").write_text("x" * 10000)
        scanner = Scanner(max_file_size=100)
        result = scanner.scan(str(tmp_path))
        assert result.files_scanned == 1

    def test_get_file_tree(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        sub = tmp_path / "src"
        sub.mkdir()
        (sub / "app.py").write_text("y = 2")
        scanner = Scanner()
        tree = scanner.get_file_tree(str(tmp_path))
        assert tree["name"] == tmp_path.name
        assert "children" in tree

    def test_get_repository_metadata(self, tmp_path) -> None:
        (tmp_path / "README.md").write_text("# Test")
        (tmp_path / "LICENSE").write_text("MIT")
        (tmp_path / ".gitignore").write_text("__pycache__/")
        scanner = Scanner()
        meta = scanner.get_repository_metadata(str(tmp_path))
        assert meta["has_readme"] is True
        assert meta["has_license"] is True
        assert meta["has_gitignore"] is True

    def test_scan_incremental(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        scanner = Scanner()
        result = scanner.scan(str(tmp_path), scan_type=ScanType.INCREMENTAL)
        assert result.scan_type == ScanType.INCREMENTAL
        assert result.status == ScanStatus.SUCCESS

    def test_scan_duration(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        scanner = Scanner()
        result = scanner.scan(str(tmp_path))
        assert result.duration_seconds >= 0
        assert result.completed_at is not None
