from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA_PATH = Path(__file__).parents[1] / "contracts/integration/event-envelope.schema.json"
EVENT_PATTERN = re.compile(r"^[a-z][a-z0-9_.-]{2,119}$")


def validate_envelope(envelope: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    required = set(schema["required"])
    missing = required - envelope.keys()
    if missing:
        raise ValueError(f"missing required fields: {sorted(missing)}")
    extra = set(envelope) - set(schema["properties"])
    if extra:
        raise ValueError(f"unexpected fields: {sorted(extra)}")
    for field in ("event_id", "source_service", "tenant_id", "actor_id", "entity_id", "correlation_id", "idempotency_key"):
        value = envelope[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
    if not isinstance(envelope["event_type"], str) or not EVENT_PATTERN.fullmatch(envelope["event_type"]):
        raise ValueError("event_type has an invalid format")
    if not isinstance(envelope["schema_version"], int) or isinstance(envelope["schema_version"], bool) or envelope["schema_version"] < 1:
        raise ValueError("schema_version must be a positive integer")
    if not isinstance(envelope["occurred_at"], str):
        raise ValueError("occurred_at must be a date-time string")
    try:
        datetime.fromisoformat(envelope["occurred_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("occurred_at must be an ISO date-time") from exc
    if not isinstance(envelope["payload"], dict):
        raise ValueError("payload must be an object")


if __name__ == "__main__":
    import sys

    for filename in sys.argv[1:]:
        validate_envelope(json.loads(Path(filename).read_text(encoding="utf-8")))
        print(f"valid: {filename}")
