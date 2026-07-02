"""
Engineering Analyzer
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .index import RepositoryIndex
from .models import Issue


@dataclass(slots=True)
class AnalysisResult:
    issues: list[Issue] = field(default_factory=list)

    score: float = 100.0


class EngineeringAnalyzer:
    def analyze(
        self,
        index: RepositoryIndex,
    ) -> AnalysisResult:

        result = AnalysisResult()

        module_count = len(index.graph.nodes())

        if module_count == 0:
            result.score = 0

        return result
