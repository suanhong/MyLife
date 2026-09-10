# MyLife v2

MyLife v2 is a replacement for the legacy Python 2.7 App Engine diary service.

## Current safety posture

- `master` remains the legacy production branch and must not be modified for v2 work.
- Recovery is complete and independent of the legacy app runtime.
- The portable backup format is `diaries.jsonl`, `images.json`, `manifest.json`, `diaries/`, and `photos/`.
- v2 development starts from this recovered data, not by redeploying the old Python 2 app.

## Target architecture

- Backend: FastAPI on Python 3.12
- Runtime: Cloud Run
- Database: Google Cloud Datastore/Firestore client
- Object storage: Google Cloud Storage
- Scheduler: Cloud Scheduler
- Mail: pluggable provider interface; Gmail API or SMTP can be implemented behind the interface
- Auth: single-user first, provider pluggable

## Development phases

1. Boot a minimal FastAPI service.
2. Define stable domain models for diaries and images.
3. Build an importer for the recovered portable backup.
4. Provide read/search endpoints for the migrated diary corpus.
5. Add daily prompt and reply ingestion.
6. Add reliable export/backup from v2.

## Non-negotiable design rules

- Backup-first: every version must preserve a simple portable export path.
- No monolithic in-memory export jobs.
- Long-running work must use pagination, retries, and resumable checkpoints.
- All image files must be content-addressable or checksum-verifiable.
- Provider credentials must not be written to portable backup artifacts.
