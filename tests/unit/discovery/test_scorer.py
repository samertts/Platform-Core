"""Unit tests for Health Scorer."""

from platform_core.discovery.scorer import HealthScorer
from platform_core.discovery.types import (
    AnalysisResult,
    ArchitectureInfo,
    CIInfo,
    DependencyInfo,
    DocumentationInfo,
    FrameworkInfo,
    HealthRating,
    HealthScore,
    LanguageInfo,
    SecurityInfo,
    TestingInfo,
)


class TestHealthScorer:
    def test_init(self) -> None:
        scorer = HealthScorer()
        assert scorer is not None

    def test_perfect_score(self) -> None:
        scorer = HealthScorer()
        analysis = AnalysisResult(
            documentation=DocumentationInfo(
                score=1.0, has_readme=True, has_changelog=True, has_license=True
            ),
            testing=TestingInfo(score=1.0, test_files=10),
            security=SecurityInfo(score=1.0, has_gitignore=True, has_security_md=True),
            architecture=ArchitectureInfo(pattern="microservices", confidence=1.0),
            dependencies=DependencyInfo(score=1.0),
            ci_cd=CIInfo(score=1.0, has_ci=True),
            language=LanguageInfo(primary="Python"),
            framework=FrameworkInfo(name="FastAPI"),
        )
        score = scorer.calculate(analysis)
        assert score.overall >= 0.9
        assert score.rating == HealthRating.EXCELLENT

    def test_zero_score(self) -> None:
        scorer = HealthScorer()
        analysis = AnalysisResult()
        score = scorer.calculate(analysis)
        assert score.overall < 0.3
        assert score.rating in (HealthRating.CRITICAL, HealthRating.POOR)

    def test_good_score(self) -> None:
        scorer = HealthScorer()
        analysis = AnalysisResult(
            documentation=DocumentationInfo(score=0.8, has_readme=True),
            testing=TestingInfo(score=0.7, test_files=5),
            security=SecurityInfo(score=0.9, has_gitignore=True),
            architecture=ArchitectureInfo(pattern="monolith", confidence=0.7),
            dependencies=DependencyInfo(score=0.6),
            ci_cd=CIInfo(score=0.8, has_ci=True),
        )
        score = scorer.calculate(analysis)
        assert 0.5 <= score.overall <= 1.0

    def test_rating_thresholds(self) -> None:
        scorer = HealthScorer()
        assert scorer._get_rating(0.95) == HealthRating.EXCELLENT
        assert scorer._get_rating(0.8) == HealthRating.GOOD
        assert scorer._get_rating(0.6) == HealthRating.FAIR
        assert scorer._get_rating(0.4) == HealthRating.POOR
        assert scorer._get_rating(0.1) == HealthRating.CRITICAL

    def test_category_breakdown(self) -> None:
        scorer = HealthScorer()
        analysis = AnalysisResult(
            documentation=DocumentationInfo(score=0.8),
            testing=TestingInfo(score=0.6),
            security=SecurityInfo(score=0.9),
            architecture=ArchitectureInfo(confidence=0.7),
            dependencies=DependencyInfo(score=0.5),
            ci_cd=CIInfo(score=0.8),
        )
        breakdown = scorer.get_category_breakdown(analysis)
        assert "documentation" in breakdown
        assert "testing" in breakdown
        assert breakdown["documentation"]["score"] == 0.8

    def test_compare_scores(self) -> None:
        scorer = HealthScorer()
        previous = HealthScore(overall=0.6, documentation=0.5, testing=0.5)
        current = HealthScore(overall=0.8, documentation=0.7, testing=0.6)
        comparison = scorer.compare_scores(current, previous)
        assert comparison["overall_change"] > 0
        assert comparison["improved"] is True

    def test_custom_weights(self) -> None:
        custom = {"security": 0.5, "testing": 0.5}
        scorer = HealthScorer(custom_weights=custom)
        analysis = AnalysisResult(
            security=SecurityInfo(score=1.0),
            testing=TestingInfo(score=1.0),
        )
        score = scorer.calculate(analysis)
        assert score.overall >= 0.9
