"""Review Manager - Manages governance reviews across all review types."""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any

from platform_core.governance.types import (
    Finding,
    FindingSeverity,
    Review,
    ReviewStatus,
    ReviewType,
)


class ReviewManager:
    """Manages governance reviews and their lifecycle."""

    def __init__(self) -> None:
        self._reviews: dict[str, Review] = {}
        self._lock = threading.RLock()

    def create_review(
        self,
        repository: str,
        review_type: ReviewType,
        reviewer: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> Review:
        review = Review(
            repository=repository,
            review_type=review_type,
            reviewer=reviewer,
            status=ReviewStatus.PENDING,
            metadata=metadata or {},
        )
        with self._lock:
            self._reviews[review.id] = review
        return review

    def get_review(self, review_id: str) -> Review | None:
        with self._lock:
            return self._reviews.get(review_id)

    def start_review(self, review_id: str) -> Review | None:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None:
                return None
            review.status = ReviewStatus.IN_PROGRESS
            review.started_at = datetime.now(timezone.utc)
            return review

    def complete_review(
        self,
        review_id: str,
        findings: list[Finding] | None = None,
        score: float = 0.0,
        summary: str = "",
    ) -> Review | None:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None:
                return None
            review.status = ReviewStatus.COMPLETED
            review.completed_at = datetime.now(timezone.utc)
            if findings is not None:
                review.findings = findings
            review.score = score
            review.summary = summary
            return review

    def fail_review(self, review_id: str, reason: str = "") -> Review | None:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None:
                return None
            review.status = ReviewStatus.FAILED
            review.completed_at = datetime.now(timezone.utc)
            review.summary = reason
            return review

    def cancel_review(self, review_id: str) -> Review | None:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None:
                return None
            review.status = ReviewStatus.CANCELLED
            review.completed_at = datetime.now(timezone.utc)
            return review

    def list_reviews(
        self,
        repository: str | None = None,
        review_type: ReviewType | None = None,
        status: ReviewStatus | None = None,
    ) -> list[Review]:
        with self._lock:
            results = list(self._reviews.values())

        if repository is not None:
            results = [r for r in results if r.repository == repository]
        if review_type is not None:
            results = [r for r in results if r.review_type == review_type]
        if status is not None:
            results = [r for r in results if r.status == status]

        return results

    def get_latest_review(
        self, repository: str, review_type: ReviewType
    ) -> Review | None:
        reviews = self.list_reviews(repository=repository, review_type=review_type)
        completed = [r for r in reviews if r.status == ReviewStatus.COMPLETED]
        if not completed:
            return None
        return max(completed, key=lambda r: r.completed_at or datetime.min.replace(tzinfo=timezone.utc))

    def get_review_summary(self, repository: str | None = None) -> dict[str, Any]:
        reviews = self.list_reviews(repository=repository)
        by_type: dict[str, int] = {}
        by_status: dict[str, int] = {}

        for r in reviews:
            rt = r.review_type.value
            by_type[rt] = by_type.get(rt, 0) + 1
            st = r.status.value
            by_status[st] = by_status.get(st, 0) + 1

        return {
            "total": len(reviews),
            "by_type": by_type,
            "by_status": by_status,
            "completed_count": by_status.get("completed", 0),
            "pending_count": by_status.get("pending", 0) + by_status.get("in_progress", 0),
        }

    def run_all_reviews(self, repository: str) -> list[Review]:
        reviews: list[Review] = []
        for review_type in ReviewType:
            review = self.create_review(repository=repository, review_type=review_type)
            self.start_review(review.id)
            review.status = ReviewStatus.COMPLETED
            review.completed_at = datetime.now(timezone.utc)
            reviews.append(review)
        return reviews

    def count(self) -> int:
        with self._lock:
            return len(self._reviews)

    def clear(self) -> None:
        with self._lock:
            self._reviews.clear()
