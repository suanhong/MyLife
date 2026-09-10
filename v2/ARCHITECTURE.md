# MyLife v2 architecture

## Non-negotiable invariants

1. The legacy production App Engine application remains untouched until cutover.
2. The independently verified portable backup is the migration source of truth.
3. Scheduled mail is idempotent: a day is marked sent only after provider acceptance.
4. Inbound replies are idempotent by Message-ID/reply token.
5. Images are validated by MIME type, stored privately, and referenced by stable IDs.
6. Export is streaming/disk-backed and resumable; no whole-archive in-memory buffer.
7. Asia/Seoul is represented by an IANA timezone, never a static UTC offset table.

## Components

- `mylife` Flask application: web UI and HTTP endpoints.
- diary repository: Datastore adapter, isolated behind an interface.
- image store: private Cloud Storage adapter.
- scheduler endpoint: invoked by Cloud Scheduler with authenticated service identity.
- outbound mail adapter: provider-neutral interface.
- inbound mail adapter: provider-specific retrieval/webhook feeding the standard MIME parser.
- portable exporter/importer: migration and disaster recovery.

## Cutover gates

Before production cutover all of these must pass: backup import count/hash validation; old diary rendering; image association; create/edit/delete; daily mail idempotency and retry; reply ingestion and Message-ID deduplication; multi-image attachment test; export/re-import round trip; authentication; scheduler authorization; rollback rehearsal.

## Email provider decision

Do not couple the domain model to a provider yet. For a single-user service, Gmail API polling with a dedicated label is a strong option because it avoids a public inbound-email webhook, but the adapter boundary keeps SMTP/inbound providers possible. Provider selection requires user authorization/configuration and is therefore a later integration gate.
