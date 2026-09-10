# MyLife v2 migration and recovery plan

## Prime directive

Do not modify or redeploy the legacy `master` application until all diary posts and original images have been independently recovered and verified.

Legacy production project: `floodin-life`
Legacy App Engine region: `asia-northeast1`
Legacy service: `floodin-life.an.r.appspot.com`

## Known legacy state

- Python 2.7 / webapp2 App Engine application.
- Posts are stored as NDB `Post` entities.
- Images are represented by NDB `UserImage` entities and original bytes are stored in the default GCS bucket.
- Daily mail is triggered by App Engine cron and sent with the legacy App Engine Mail API.
- Replies are received by the legacy App Engine inbound mail service.
- Dropbox backup uses a stored bearer access token.
- Manual ZIP export repeatedly stalls around image 136 of 252.

## Recovery order

1. Inventory every `Post` and `UserImage` entity without changing data.
2. Identify the image at/after the repeatable export failure boundary.
3. Export post metadata separately from image bytes so one corrupt/unreadable image cannot prevent diary recovery.
4. Export images independently and record success/failure for every image.
5. Produce a manifest containing counts, filenames, dates, byte sizes and SHA-256 hashes.
6. Verify recovered post count and image count against Datastore metadata.
7. Only after verification, build/import into MyLife v2.

## v2 portability requirement

A complete backup must be restorable without App Engine, Dropbox, or MyLife itself. Target backup layout:

```
backup-YYYY-MM-DD/
  manifest.json
  diaries.json
  diaries/
    YYYY-MM-DD.md
  photos/
    YYYY-MM-DD-N.ext
```

Each manifest image entry should include at least filename, diary date, original filename, byte size, SHA-256 and backup status.

## Export failure hypothesis

The legacy exporter builds one ZIP entirely in memory and reads every original image sequentially. A repeatable stop at approximately the same image strongly suggests either a problematic image/object or a resource/runtime limit. Recovery tooling must therefore never require all images to succeed in one request.
