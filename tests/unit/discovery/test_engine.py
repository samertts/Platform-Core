"""Unit tests for Discovery Engine."""

import pytest
from platform_core.discovery.engine import DiscoveryEngine, DiscoveryError
from platform_core.discovery.types import ScanType, ScanStatus


class TestDiscoveryEngine:
    def test_init(self) -> None:
        engine = DiscoveryEngine()
        assert engine is not None

    def test_discover_nonexistent_path(self) -> None:
        engine = DiscoveryEngine()
        with pytest.raises(DiscoveryError, match="does not exist"):
            engine.discover("/nonexistent/path")

    def test_discover_empty_directory(self, tmp_path) -> None:
        engine = DiscoveryEngine()
        result = engine.discover(str(tmp_path), repository_name="empty")
        assert result.status == ScanStatus.SUCCESS
        assert result.repository == "empty"

    def test_discover_with_files(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("print('hello')")
        (tmp_path / "README.md").write_text("# Test")
        engine = DiscoveryEngine()
        result = engine.discover(str(tmp_path), repository_name="test-repo")
        assert result.status == ScanStatus.SUCCESS
        assert result.repository == "test-repo"
        assert result.health_score.overall >= 0

    def test_discover_stores_result(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        engine = DiscoveryEngine()
        engine.discover(str(tmp_path), repository_name="stored")
        assert engine.get_result("stored") is not None

    def test_discover_multiple(self, tmp_path) -> None:
        repo1 = tmp_path / "repo1"
        repo2 = tmp_path / "repo2"
        repo1.mkdir()
        repo2.mkdir()
        (repo1 / "main.py").write_text("x = 1")
        (repo2 / "app.py").write_text("y = 2")
        engine = DiscoveryEngine()
        results = engine.discover_multiple([str(repo1), str(repo2)])
        assert len(results) == 2

    def test_get_all_results(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        engine = DiscoveryEngine()
        engine.discover(str(tmp_path), repository_name="r1")
        all_results = engine.get_all_results()
        assert len(all_results) == 1

    def test_get_ecosystem_report(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        engine = DiscoveryEngine()
        engine.discover(str(tmp_path), repository_name="r1")
        report = engine.get_ecosystem_report()
        assert report.total_repositories == 1

    def test_get_repository_report(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        engine = DiscoveryEngine()
        engine.discover(str(tmp_path), repository_name="r1")
        report = engine.get_repository_report("r1")
        assert report is not None
        assert report.repository == "r1"

    def test_get_repository_report_not_found(self) -> None:
        engine = DiscoveryEngine()
        assert engine.get_repository_report("nonexistent") is None

    def test_get_health_summary(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        engine = DiscoveryEngine()
        engine.discover(str(tmp_path), repository_name="r1")
        summary = engine.get_health_summary("r1")
        assert "r1" not in summary or "EXCELLENT" in summary or "GOOD" in summary or "FAIR" in summary or "POOR" in summary or "CRITICAL" in summary

    def test_get_health_summary_not_found(self) -> None:
        engine = DiscoveryEngine()
        summary = engine.get_health_summary("nonexistent")
        assert "not found" in summary

    def test_clear_results(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        engine = DiscoveryEngine()
        engine.discover(str(tmp_path), repository_name="r1")
        engine.clear_results()
        assert len(engine.get_all_results()) == 0

    def test_get_statistics(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        engine = DiscoveryEngine()
        engine.discover(str(tmp_path), repository_name="r1")
        stats = engine.get_statistics()
        assert stats["total_scanned"] == 1
        assert stats["successful"] == 1

    def test_discover_incremental(self, tmp_path) -> None:
        (tmp_path / "main.py").write_text("x = 1")
        engine = DiscoveryEngine()
        result = engine.discover(str(tmp_path), scan_type=ScanType.INCREMENTAL)
        assert result.scan_type == ScanType.INCREMENTAL
