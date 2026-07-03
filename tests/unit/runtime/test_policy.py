from __future__ import annotations

import json
import os
import tempfile
from typing import Any

from platform_core.runtime.policy.engine import Policy, PolicyEngine, PolicyResult


class TestPolicyEngine:
    def test_init(self) -> None:
        engine = PolicyEngine()
        assert engine.get_active_policies() == []

    def test_add_policy(self) -> None:
        engine = PolicyEngine()
        policy = Policy(
            id="test-1",
            name="Test Policy",
            type="access_control",
            enforcement="enforcing",
            rules=[{"condition": "role:admin", "effect": "allow"}],
        )
        engine.add_policy(policy)
        assert len(engine.get_active_policies()) == 1

    def test_remove_policy(self) -> None:
        engine = PolicyEngine()
        policy = Policy(
            id="test-1",
            name="Test",
            type="general",
            enforcement="enforcing",
            rules=[],
        )
        engine.add_policy(policy)
        assert engine.remove_policy("test-1")
        assert not engine.remove_policy("nonexistent")

    def test_evaluate_allow(self) -> None:
        engine = PolicyEngine()
        policy = Policy(
            id="allow-all",
            name="Allow All",
            type="access_control",
            enforcement="enforcing",
            rules=[{"condition": "role:admin", "effect": "allow"}],
        )
        engine.add_policy(policy)
        result = engine.evaluate({"role": "admin"})
        assert result.allowed

    def test_evaluate_deny(self) -> None:
        engine = PolicyEngine()
        policy = Policy(
            id="deny-user",
            name="Deny User",
            type="access_control",
            enforcement="enforcing",
            rules=[{"condition": "role:user", "effect": "deny"}],
        )
        engine.add_policy(policy)
        result = engine.evaluate({"role": "user"})
        assert not result.allowed

    def test_evaluate_advisory(self) -> None:
        engine = PolicyEngine()
        policy = Policy(
            id="advisory",
            name="Advisory",
            type="security",
            enforcement="advisory",
            rules=[{"condition": "role:guest", "effect": "deny"}],
        )
        engine.add_policy(policy)
        result = engine.evaluate({"role": "guest"})
        assert result.allowed

    def test_load_json_policies(self) -> None:
        engine = PolicyEngine()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(
                {
                    "policies": [
                        {
                            "id": "loaded-1",
                            "name": "Loaded Policy",
                            "type": "general",
                            "enforcement": "enforcing",
                            "rules": [],
                        }
                    ]
                },
                f,
            )
            f.flush()
            try:
                count = engine.load_policies(f.name)
                assert count == 1
            finally:
                os.unlink(f.name)

    def test_authorization_hook(self) -> None:
        engine = PolicyEngine()

        def hook(ctx: dict[str, Any]) -> PolicyResult:
            if ctx.get("blocked"):
                return PolicyResult(allowed=False, reason="blocked by hook")
            return PolicyResult(allowed=True)

        engine.register_authorization_hook(hook)
        result = engine.evaluate({"blocked": True})
        assert not result.allowed

        result = engine.evaluate({"blocked": False})
        assert result.allowed
