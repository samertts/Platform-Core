"""Discovery Engine - Orchestrates scanning, analysis, scoring, and reporting."""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from platform_core.discovery.analyzers import run_all_analyzers
from platform_core.discovery.reporter import Reporter
from platform_core.discovery.scanner import Scanner
from platform_core.discovery.scorer import HealthScorer
from platform_core.discovery.types import (
    AnalysisResult,
    DiscoveryResult,
    EcosystemReport,
    HealthScore,
    RepositoryReport,
    ScanResult,
    ScanStatus,
    ScanType,
)


class DiscoveryError(Exception):
    pass


class DiscoveryEngine:
    """Orchestrates the full discovery workflow: scan, analyze, score, report."""

    def __init__(
        self,
        scanner: Scanner | None = None,
        scorer: HealthScorer | None = None,
        reporter: Reporter | None = None,
    ) -> None:
        self._scanner = scanner or Scanner()
        self._scorer = scorer or HealthScorer()
        self._reporter = reporter or Reporter()
        self._results: dict[str, DiscoveryResult] = {}
        self._lock = threading.RLock()

    def discover(
        self,
        repository_path: str,
        repository_name: str = "",
        scan_type: ScanType = ScanType.FULL,
    ) -> DiscoveryResult:
        root = Path(repository_path)
        if not root.exists():
            raise DiscoveryError(f"Path does not exist: {repository_path}")
        if not root.is_dir():
            raise DiscoveryError(f"Path is not a directory: {repository_path}")

        name = repository_name or root.name

        result = DiscoveryResult(
            repository=name,
            scan_type=scan_type,
            started_at=datetime.now(timezone.utc),
            status=ScanStatus.RUNNING,
        )

        try:
            scan_result = self._scanner.scan(
                repository_path, scan_type=scan_type, repository=name
            )
            result.scan = scan_result

            files = self._scanner._collect_files(root)
            analysis = run_all_analyzers(repository_path, files)
            analysis.repository = name
            analysis.scan_id = scan_result.id
            result.analysis = analysis

            health = self._scorer.calculate(analysis)
            result.health_score = health

            result.status = ScanStatus.SUCCESS
        except Exception as e:
            result.status = ScanStatus.FAILED
            result.scan.errors.append(str(e))

        result.completed_at = datetime.now(timezone.utc)
        result.duration_seconds = (
            result.completed_at - result.started_at
        ).total_seconds()

        with self._lock:
            self._results[name] = result

        return result

    def discover_multiple(
        self,
        paths: list[str],
        scan_type: ScanType = ScanType.FULL,
    ) -> list[DiscoveryResult]:
        results: list[DiscoveryResult] = []
        for path in paths:
            try:
                result = self.discover(path, scan_type=scan_type)
                results.append(result)
            except DiscoveryError:
                continue
        return results

    def get_result(self, repository: str) -> DiscoveryResult | None:
        with self._lock:
            return self._results.get(repository)

    def get_all_results(self) -> list[DiscoveryResult]:
        with self._lock:
            return list(self._results.values())

    def get_ecosystem_report(self) -> EcosystemReport:
        results = self.get_all_results()
        return self._reporter.generate_ecosystem_report(results)

    def get_repository_report(self, repository: str) -> RepositoryReport | None:
        result = self.get_result(repository)
        if result is None:
            return None
        return self._reporter.generate_repository_report(result)

    def get_health_summary(self, repository: str) -> str:
        result = self.get_result(repository)
        if result is None:
            return f"Repository '{repository}' not found"
        return self._reporter.format_health_summary(result.health_score)

    def clear_results(self) -> None:
        with self._lock:
            self._results.clear()

    def get_statistics(self) -> dict[str, Any]:
        results = self.get_all_results()
        successful = [r for r in results if r.status == ScanStatus.SUCCESS]
        scores = [r.health_score.overall for r in successful]

        return {
            "total_scanned": len(results),
            "successful": len(successful),
            "failed": len(results) - len(successful),
            "average_score": round(sum(scores) / len(scores), 3) if scores else 0.0,
            "best_score": round(max(scores), 3) if scores else 0.0,
            "worst_score": round(min(scores), 3) if scores else 0.0,
        }
