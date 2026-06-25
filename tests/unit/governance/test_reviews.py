"""Unit tests for Review Manager."""

import pytest
from platform_core.governance.reviews import ReviewManager
from platform_core.governance.types import ReviewStatus, ReviewType


class TestReviewManager:
    def test_init(self) -> None:
        rm = ReviewManager()
        assert rm.count() == 0

    def test_create_review(self) -> None:
        rm = ReviewManager()
        r = rm.create_review("repo", ReviewType.ARCHITECTURE, reviewer="alice")
        assert r.repository == "repo"
        assert r.review_type == ReviewType.ARCHITECTURE
        assert r.status == ReviewStatus.PENDING

    def test_start_review(self) -> None:
        rm = ReviewManager()
        r = rm.create_review("repo", ReviewType.SECURITY)
        started = rm.start_review(r.id)
        assert started is not None
        assert started.status == ReviewStatus.IN_PROGRESS

    def test_complete_review(self) -> None:
        rm = ReviewManager()
        r = rm.create_review("repo", ReviewType.API)
        rm.start_review(r.id)
        completed = rm.complete_review(r.id, score=0.85, summary="All good")
        assert completed is not None
        assert completed.status == ReviewStatus.COMPLETED
        assert completed.score == 0.85

    def test_fail_review(self) -> None:
        rm = ReviewManager()
        r = rm.create_review("repo", ReviewType.SECURITY)
        rm.start_review(r.id)
        failed = rm.fail_review(r.id, reason="Error occurred")
        assert failed is not None
        assert failed.status == ReviewStatus.FAILED

    def test_cancel_review(self) -> None:
        rm = ReviewManager()
        r = rm.create_review("repo", ReviewType.PERFORMANCE)
        cancelled = rm.cancel_review(r.id)
        assert cancelled is not None
        assert cancelled.status == ReviewStatus.CANCELLED

    def test_list_reviews(self) -> None:
        rm = ReviewManager()
        rm.create_review("repo-a", ReviewType.ARCHITECTURE)
        rm.create_review("repo-b", ReviewType.SECURITY)
        rm.create_review("repo-a", ReviewType.API)
        assert len(rm.list_reviews()) == 3
        assert len(rm.list_reviews(repository="repo-a")) == 2
        assert len(rm.list_reviews(review_type=ReviewType.SECURITY)) == 1

    def test_get_latest_review(self) -> None:
        rm = ReviewManager()
        r1 = rm.create_review("repo", ReviewType.ARCHITECTURE)
        rm.start_review(r1.id)
        rm.complete_review(r1.id, score=0.9, summary="Good")
        r2 = rm.create_review("repo", ReviewType.SECURITY)
        rm.start_review(r2.id)
        rm.complete_review(r2.id, score=0.8, summary="OK")
        latest = rm.get_latest_review("repo", ReviewType.ARCHITECTURE)
        assert latest is not None
        assert latest.review_type == ReviewType.ARCHITECTURE

    def test_run_all_reviews(self) -> None:
        rm = ReviewManager()
        reviews = rm.run_all_reviews("repo")
        assert len(reviews) == len(ReviewType)

    def test_get_review_summary(self) -> None:
        rm = ReviewManager()
        rm.run_all_reviews("repo")
        summary = rm.get_review_summary("repo")
        assert summary["total"] == len(ReviewType)

    def test_clear(self) -> None:
        rm = ReviewManager()
        rm.create_review("repo", ReviewType.ARCHITECTURE)
        rm.clear()
        assert rm.count() == 0
