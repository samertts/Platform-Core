from __future__ import annotations


class CancellationToken:
    """
    Cooperative cancellation token.

    This object is intentionally lightweight and contains no
    synchronization primitives at this stage. Thread-safe
    implementations may be introduced later without changing
    the public contract.
    """

    __slots__ = ("_cancelled",)

    def __init__(self) -> None:
        self._cancelled = False

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    def cancel(self) -> None:
        self._cancelled = True
