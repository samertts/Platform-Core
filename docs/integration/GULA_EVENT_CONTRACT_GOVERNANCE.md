# GULA Integration Event Contract Governance

`Platform-Core` owns the versioned cross-repository event envelope. GULA remains the clinical system of record and validates every received envelope before dispatching it to a domain handler.

The envelope requires `event_id`, `event_type`, `schema_version`, `source_service`, `tenant_id`, `occurred_at`, `actor_id`, `entity_id`, `correlation_id`, `idempotency_key`, and an object `payload`. Unknown top-level fields are invalid. Timestamps must be timezone-aware, and event types must use the lower-case dotted naming convention.

A producer must not publish a new schema version without a compatibility note and contract tests. A consumer must reject unsupported versions rather than guessing. Replayed events must be recognized by `event_id` or `idempotency_key` and must not create duplicate side effects.

The envelope is transport-neutral. It may be delivered through HTTP, a durable queue, or an offline synchronization channel, but the transport must preserve authentication, tenant context, correlation identifiers, and audit metadata. Payloads containing clinical results remain pending until GULA applies sample matching and clinical authorization.

The canonical schema is `contracts/integration/event-envelope.schema.json`. Language-specific implementations must be generated or validated against that schema and tested in CI.
