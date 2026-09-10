# MyLife v2 architecture

The existing FastAPI/Cloud Run backend is the canonical v2 implementation.

Production invariants: legacy `master` and App Engine remain untouched until cutover; the verified recovered backup is the migration source of truth; daily email is marked sent only after provider acceptance; replies are deduplicated by Message-ID and routed by an opaque reply token; image attachments require MIME, size, and signature validation and remain private in Cloud Storage; Asia/Seoul uses the IANA timezone; exports are disk/stream based rather than whole-archive memory buffers.

The verified legacy backup has SHA-256 `8edb7cfc8bd196d238b0044e146aa0742a01175824c707c4cc673419f01713fb` and expected counts 2,822 posts, 252 UserImage/original images, and 252 image references.

No production deployment is configured. Staging must be a separate Cloud Run service and v2-only Datastore kinds/storage namespace. Live email integration and staging migration require user authorization/approval and are explicit gates.
