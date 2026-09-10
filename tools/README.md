# Recovery tools

This directory is reserved for read-only recovery/migration tooling for the legacy MyLife deployment.

## Safety rules

- Tools must not delete or mutate legacy `Post`, `UserImage`, `Slug`, or storage objects.
- Diary metadata and image bytes must be recoverable independently.
- One bad image must be reported and skipped rather than aborting the entire recovery.
- Every recovered image will eventually be hashed and represented in a manifest.
- Do not deploy experimental v2 application code over the production Python 2.7 service.

The first executable recovery tool will be added after the production data-access path is selected and tested against a read-only inventory operation.
