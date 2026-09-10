# MyLife v2

Modern replacement for the legacy single-user MyLife diary service.

## Safety boundary

The legacy `master` branch and production App Engine service are not deployment targets for v2 development. Build and test v2 independently. Migration must use the independently verified portable backup before any production cutover.

## Initial architecture

- Python 3.12 / Flask
- Cloud Run container
- Google Cloud Datastore for diary metadata
- Google Cloud Storage for private image objects
- Cloud Scheduler for scheduled jobs
- email integration added as a separate adapter so provider choice does not leak into diary domain logic

## Local test

```sh
python -m pip install -e '.[dev]'
pytest
python app.py
```

Then open `http://localhost:8080/healthz`.

## Deployment policy

No automatic production deployment is configured at this stage. CI may build/test the v2 code, but deployment remains a separate explicit step until migration and mail-flow tests pass.
