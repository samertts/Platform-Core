"""
NHDOS Frontend Hooks

Reusable hooks for frontend state management
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Callable
from ..types.base import ApiResponse, PaginatedResponse


@dataclass
class UseState:
    """State management hook."""
    value: Any = None
    setter: Optional[Callable] = None

    def update(self, new_value: Any):
        self.value = new_value
        if self.setter:
            self.setter(new_value)


@dataclass
class UseEffect:
    """Side effect hook."""
    dependencies: list[Any] = field(default_factory=list)
    cleanup: Optional[Callable] = None
    effect: Optional[Callable] = None


@dataclass
class UseCallback:
    """Memoized callback hook."""
    callback: Optional[Callable] = None
    dependencies: list[Any] = field(default_factory=list)


@dataclass
class UseMemo:
    """Memoized value hook."""
    value: Any = None
    dependencies: list[Any] = field(default_factory=list)


@dataclass
class UseQuery:
    """Data fetching hook."""
    data: Any = None
    error: Optional[str] = None
    loading: bool = False
    refetch: Optional[Callable] = None


@dataclass
class UseMutation:
    """Data mutation hook."""
    data: Any = None
    error: Optional[str] = None
    loading: bool = False
    mutate: Optional[Callable] = None


def use_state(initial_value: Any = None) -> UseState:
    return UseState(value=initial_value)


def use_effect(effect: Callable, dependencies: list[Any] = None) -> UseEffect:
    return UseEffect(dependencies=dependencies or [], effect=effect)


def use_callback(callback: Callable, dependencies: list[Any] = None) -> UseCallback:
    return UseCallback(callback=callback, dependencies=dependencies or [])


def use_memo(factory: Callable, dependencies: list[Any] = None) -> UseMemo:
    return UseMemo(value=factory(), dependencies=dependencies or [])


def use_query(fetcher: Callable, *args, **kwargs) -> UseQuery:
    return UseQuery(loading=True, refetch=lambda: fetcher(*args, **kwargs))


def use_mutate(mutation: Callable) -> UseMutation:
    return UseMutation(mutate=mutation)
