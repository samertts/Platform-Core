from copy import deepcopy

import pytest

from scripts.validate_event_envelope import validate_envelope


BASE = {
    "event_id": "event-1",
    "event_type": "platform.diagnostic.reported",
    "schema_version": 1,
    "source_service": "govlab-platform",
    "tenant_id": "tenant-1",
    "occurred_at": "2026-08-13T10:00:00Z",
    "actor_id": "operator-1",
    "entity_id": "entity-1",
    "correlation_id": "correlation-1",
    "idempotency_key": "idem-1",
    "payload": {"status": "ok"},
}


@pytest.mark.parametrize(
    "event_type,source_service,payload",
    [
        ("sample.custody.transitioned", "receipt-and-delivery", {"sample_id": "s1"}),
        ("device.observation.pending", "lablink-core", {"status": "pending_review"}),
        ("identity.subject.mapped", "identity-credential", {"subject_id": "sub-1"}),
        ("workforce.attendance.recorded", "inwp", {"event_id": "attendance-1"}),
        ("frontend.sync.requested", "gula-front-end", {"action_id": "action-1"}),
        ("correspondence.issued", "oglg", {"letter_id": "letter-1"}),
        ("platform.diagnostic.reported", "govlab-platform", {"healthy": True}),
    ],
)
def test_all_registered_services_emit_valid_envelopes(event_type, source_service, payload):
    envelope = deepcopy(BASE)
    envelope.update(event_type=event_type, source_service=source_service, payload=payload)
    validate_envelope(envelope)


def test_unknown_fields_are_rejected():
    envelope = deepcopy(BASE)
    envelope["clinical_approval"] = "approved"
    with pytest.raises(ValueError, match="unexpected fields"):
        validate_envelope(envelope)


def test_invalid_timestamp_is_rejected():
    envelope = deepcopy(BASE)
    envelope["occurred_at"] = "not-a-date"
    with pytest.raises(ValueError, match="ISO date-time"):
        validate_envelope(envelope)
