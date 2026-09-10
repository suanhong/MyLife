# Implementation roadmap

## Completed in foundation branch

- Python 3.12 / Flask project and Cloud Run container
- CI test/container-build workflow with no deploy credentials
- repository abstraction plus Datastore adapter
- private Cloud Storage image adapter
- portable backup inspection/migration validation
- daily prompt idempotency rule and provider-neutral mail boundary
- MIME reply parsing, Message-ID deduplication, conservative quote stripping
- anniversary old-entry selection and Asia/Seoul timezone handling
- basic diary CRUD HTTP API
- backup writer and security/cutover documentation

## Next code-only work

- legacy Post/UserImage reference mapper from portable backup
- migration dry-run report
- Datastore-backed sent-message/idempotency stores
- authenticated internal scheduler route
- image metadata repository and thumbnail pipeline
- HTML UI for browse/edit/delete

## User integration gates

The first user action is intentionally deferred until a provider/account choice or cloud authorization is required. Likely gates are: choosing/authorizing the email transport (Gmail API versus another provider), providing the verified backup to a staging import environment, and approving creation/deployment of separate staging Google Cloud resources. None of these should modify the legacy App Engine service.
