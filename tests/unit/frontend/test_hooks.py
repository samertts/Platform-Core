"""
Tests for NHDOS Frontend Hooks
"""

import sys
sys.path.insert(0, '/tmp')

from platform_core.frontend.hooks import (
    UseState, UseEffect, UseCallback, UseMemo, UseQuery, UseMutation,
    use_state, use_effect, use_callback, use_memo, use_query, use_mutate
)


class TestHooks:
    def test_use_state(self):
        state = use_state(42)
        assert state.value == 42

    def test_use_state_update(self):
        state = use_state(42)
        state.update(100)
        assert state.value == 100

    def test_use_effect(self):
        effect = use_effect(lambda: print("effect"), [1, 2])
        assert effect.dependencies == [1, 2]

    def test_use_callback(self):
        callback = use_callback(lambda: "result", [1])
        assert callback.dependencies == [1]

    def test_use_memo(self):
        memo = use_memo(lambda: 42, [1])
        assert memo.value == 42

    def test_use_query(self):
        query = use_query(lambda: "data")
        assert query.loading is True
        assert query.refetch is not None

    def test_use_mutate(self):
        mutation = use_mutate(lambda: "mutated")
        assert mutation.mutate is not None
