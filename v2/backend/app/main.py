from __future__ import annotations

from datetime import date
from pathlib import Path, PurePosixPath

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from google.cloud import storage as gcs

from .datastore_repository import DatastoreDiaryRepository
from .models import DiaryEntry, DiaryEntryList, HealthCheck, RepositoryStats
from .settings import get_settings
from .storage import DiaryRepository, InMemoryDiaryRepository

BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()

app = FastAPI(
    title="MyLife v2",
    version="0.2.0",
    description="Private single-user diary service protected by Cloud Run IAP.",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


def build_repository() -> DiaryRepository:
    if settings.environment == "production" or settings.project_id:
        return DatastoreDiaryRepository(
            project_id=settings.project_id,
            namespace=settings.datastore_namespace,
        )
    return InMemoryDiaryRepository()


repository: DiaryRepository = build_repository()


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health", response_model=HealthCheck)
@app.get("/healthz", response_model=HealthCheck, include_in_schema=False)
def health() -> HealthCheck:
    return HealthCheck()


@app.get("/api/stats", response_model=RepositoryStats)
def stats() -> RepositoryStats:
    return repository.stats()


@app.get("/api/entries", response_model=DiaryEntryList)
def list_entries(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    q: str | None = Query(default=None, min_length=1, max_length=100),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> DiaryEntryList:
    if date_from and date_to and date_from > date_to:
        raise HTTPException(status_code=422, detail="date_from must not be later than date_to")
    entries, total = repository.list_entries(
        limit=limit,
        offset=offset,
        query_text=q.strip() if q else None,
        date_from=date_from,
        date_to=date_to,
    )
    return DiaryEntryList(entries=entries, total=total, limit=limit, offset=offset)


@app.get("/api/entries/{entry_id}", response_model=DiaryEntry)
def get_entry(entry_id: str) -> DiaryEntry:
    entry = repository.get_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    return entry


@app.get("/api/images/{image_ref:path}")
def get_image(image_ref: str) -> Response:
    if not settings.storage_bucket:
        raise HTTPException(status_code=503, detail="Image storage is not configured")
    image = repository.get_image(image_ref)
    if image is None or not image.filename:
        raise HTTPException(status_code=404, detail="Image metadata not found")

    # Recovered images are uploaded under a dedicated v2 prefix. basename
    # prevents imported metadata from escaping that prefix.
    filename = PurePosixPath(image.filename.replace("\\", "/")).name
    object_name = "/".join(part.strip("/") for part in (settings.image_prefix, filename) if part)
    blob = gcs.Client(project=settings.project_id).bucket(settings.storage_bucket).blob(object_name)
    if not blob.exists():
        raise HTTPException(status_code=404, detail="Image file not found in Cloud Storage")
    data = blob.download_as_bytes()
    return Response(
        content=data,
        media_type=image.content_type or blob.content_type or "application/octet-stream",
        headers={"Cache-Control": "private, max-age=3600"},
    )
