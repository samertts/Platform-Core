from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


@dataclass
class Policy:
    id: str
    name: str
    type: str
    enforcement: str
    rules: list[dict[str, Any]]
    status: str = "active"
    priority: int = 0
    scope: str = "platform"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PolicyResult:
    allowed: bool
    policy_id: str = ""
    reason: str = ""
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    allowed: bool
    results: list[PolicyResult] = field(default_factory=list)
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def denied_results(self) -> list[PolicyResult]:
        return [r for r in self.results if not r.allowed]


class PolicyEngine:
    """Policy loading, evaluation, and enforcement."""

    def __init__(self) -> None:
        self._policies: dict[str, Policy] = {}
        self._authorization_hooks: list[Callable[[dict[str, Any]], PolicyResult]] = []
        self._governance_hooks: list[Callable[[dict[str, Any]], PolicyResult]] = []
        self._lock = threading.Lock()

    def load_policies(self, source: str) -> int:
        count = 0
        path = Path(source)

        if path.is_file():
            count = self._load_file(path)
        elif path.is_dir():
            for file_path in sorted(path.glob("*.json")):
                count += self._load_file(file_path)
            for file_path in sorted(path.glob("*.yaml")):
                count += self._load_file(file_path)
            for file_path in sorted(path.glob("*.yml")):
                count += self._load_file(file_path)

        return count

    def _load_file(self, path: Path) -> int:
        try:
            content = path.read_text(encoding="utf-8")
            if path.suffix == ".json":
                data = json.loads(content)
            elif path.suffix in (".yaml", ".yml"):
                data = self._parse_yaml(content)
            else:
                return 0

            if isinstance(data, list):
                policies_data = data
            elif isinstance(data, dict) and "policies" in data:
                policies_data = data["policies"]
            else:
                policies_data = [data]

            count = 0
            for policy_data in policies_data:
                if isinstance(policy_data, dict) and "id" in policy_data:
                    policy = Policy(
                        id=policy_data["id"],
                        name=policy_data.get("name", ""),
                        type=policy_data.get("type", "general"),
                        enforcement=policy_data.get("enforcement", "advisory"),
                        rules=policy_data.get("rules", []),
                        priority=policy_data.get("priority", 0),
                        scope=policy_data.get("scope", "platform"),
                    )
                    with self._lock:
                        self._policies[policy.id] = policy
                    count += 1

            return count
        except Exception:
            return 0

    def _parse_yaml(self, content: str) -> Any:
        try:
            import yaml

            return yaml.safe_load(content)
        except ImportError:
            return self._parse_simple_yaml(content)

    def _parse_simple_yaml(self, content: str) -> Any:
        result: dict[str, Any] = {}
        current_section: dict[str, Any] = result
        section_stack: list[tuple[int, dict[str, Any]]] = [(0, result)]

        for line in content.splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue

            indent = len(line) - len(line.lstrip())
            stripped = line.strip()

            while section_stack and indent <= section_stack[-1][0] and len(section_stack) > 1:
                section_stack.pop()
            current_section = section_stack[-1][1]

            if ":" in stripped:
                key, _, value = stripped.partition(":")
                key = key.strip()
                value = value.strip()

                if value:
                    current_section[key] = self._parse_yaml_value(value)
                else:
                    new_section: dict[str, Any] = {}
                    current_section[key] = new_section
                    section_stack.append((indent, new_section))

        return result

    def _parse_yaml_value(self, value: str) -> Any:
        if value.lower() in ("true", "yes"):
            return True
        if value.lower() in ("false", "no"):
            return False
        if value.lower() in ("null", "none"):
            return None
        try:
            return int(value)
        except ValueError:
            pass
        return value

    def evaluate(self, context: dict[str, Any]) -> EvaluationResult:
        results: list[PolicyResult] = []

        with self._lock:
            active_policies = sorted(
                self._policies.values(),
                key=lambda p: p.priority,
                reverse=True,
            )

        for policy in active_policies:
            if policy.status != "active":
                continue
            if policy.enforcement == "audit_only":
                continue

            result = self._evaluate_policy(policy, context)
            results.append(result)

            if policy.enforcement == "enforcing" and not result.allowed:
                return EvaluationResult(
                    allowed=False,
                    results=results,
                )

        for hook in self._authorization_hooks:
            try:
                hook_result = hook(context)
                results.append(hook_result)
                if not hook_result.allowed:
                    return EvaluationResult(allowed=False, results=results)
            except Exception:
                pass

        return EvaluationResult(allowed=True, results=results)

    def _evaluate_policy(
        self, policy: Policy, context: dict[str, Any]
    ) -> PolicyResult:
        for rule in policy.rules:
            condition = rule.get("condition", "")
            effect = rule.get("effect", "allow")

            if self._evaluate_condition(condition, context):
                if effect == "deny":
                    return PolicyResult(
                        allowed=False,
                        policy_id=policy.id,
                        reason=rule.get("reason", f"Policy {policy.name} denied access"),
                    )

        return PolicyResult(
            allowed=True,
            policy_id=policy.id,
            reason=f"Policy {policy.name} passed",
        )

    def _evaluate_condition(self, condition: str, context: dict[str, Any]) -> bool:
        if not condition:
            return False

        try:
            if "==" in condition:
                left, _, right = condition.partition("==")
                left = left.strip()
                right = right.strip().strip("'\"")
                context_value = context.get(left)
                return str(context_value) == right
            elif "!=" in condition:
                left, _, right = condition.partition("!=")
                left = left.strip()
                right = right.strip().strip("'\"")
                context_value = context.get(left)
                return str(context_value) != right
            elif "in" in condition:
                parts = condition.split("in")
                if len(parts) == 2:
                    value = parts[0].strip().strip("'\"")
                    collection = context.get(parts[1].strip())
                    if isinstance(collection, (list, set)):
                        return value in collection
            elif condition.startswith("role:"):
                required_role = condition[5:].strip()
                user_role = context.get("role", "")
                return str(user_role) == required_role
        except Exception:
            return False

        return False

    def register_authorization_hook(
        self, hook: Callable[[dict[str, Any]], PolicyResult]
    ) -> None:
        with self._lock:
            self._authorization_hooks.append(hook)

    def register_governance_hook(
        self, hook: Callable[[dict[str, Any]], PolicyResult]
    ) -> None:
        with self._lock:
            self._governance_hooks.append(hook)

    def get_active_policies(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "id": p.id,
                    "name": p.name,
                    "type": p.type,
                    "enforcement": p.enforcement,
                    "status": p.status,
                    "priority": p.priority,
                    "scope": p.scope,
                }
                for p in self._policies.values()
                if p.status == "active"
            ]

    def add_policy(self, policy: Policy) -> None:
        with self._lock:
            self._policies[policy.id] = policy

    def remove_policy(self, policy_id: str) -> bool:
        with self._lock:
            if policy_id in self._policies:
                del self._policies[policy_id]
                return True
            return False

    def get_policy(self, policy_id: str) -> Policy | None:
        with self._lock:
            return self._policies.get(policy_id)
