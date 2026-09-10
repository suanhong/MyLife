# Deployment

No automatic deployment is configured. The first deployment must be a separate Cloud Run staging service with a v2-only Datastore namespace and private Storage location/prefix. Do not route the legacy App Engine hostname or cron endpoints to v2 during validation.

Before cutover: verify/import the exact recovered backup; validate counts and image associations; test browse/read, reply ingestion, multi-image attachments, daily send retry/idempotency, export/re-import, authentication, scheduler IAM, and rollback. The legacy App Engine service remains the rollback target until v2 has completed an agreed validation period.
