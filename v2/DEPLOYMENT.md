# Deployment plan

No deployment is performed by CI yet.

## Staging first

Deploy v2 as a separate Cloud Run service (for example `mylife-v2-staging`). Do not route the legacy App Engine hostname to it and do not reuse the legacy cron endpoints during validation.

Required configuration will include a Google Cloud project, a private image bucket, service identity permissions, authenticated scheduler calls, and an email-provider credential/authorization flow.

## Production gate

Production cutover is intentionally blocked until the verified portable backup has been imported into staging and the count/hash, image associations, web CRUD, daily-email retry, reply ingestion, attachment, export/re-import, authentication, and rollback tests all pass.

The legacy App Engine service remains the rollback target until v2 has operated successfully through an agreed validation period.
