# Security boundaries

MyLife is a private single-user diary and should be treated as sensitive personal data.

- Cloud Storage image objects remain private; no public ACLs.
- Production web routes require authentication before cutover.
- Scheduler/internal endpoints require authenticated service identity, not secret query parameters.
- Email credentials/tokens belong in managed secrets or provider authorization storage, never source control.
- Inbound mail is deduplicated and image attachments are accepted only when their MIME type is `image/*`; further size/decoder validation is required before production.
- Migration tools must not export legacy Settings secrets by default.
- CI has read-only repository permissions and no production deployment credentials.
