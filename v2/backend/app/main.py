from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from .datastore_repository import DatastoreDiaryRepository
from .models import DiaryEntry, DiaryEntryList, HealthCheck, RepositoryStats
from .settings import get_settings
from .storage import DiaryRepository, InMemoryDiaryRepository

app = FastAPI(
    title="MyLife v2",
    version="0.1.0",
    description="Modern replacement for the legacy MyLife diary service.",
)


def build_repository() -> DiaryRepository:
    settings = get_settings()
    if settings.environment == "production" or settings.project_id:
        return DatastoreDiaryRepository(
            project_id=settings.project_id,
            namespace=settings.datastore_namespace,
        )
    return InMemoryDiaryRepository()


repository: DiaryRepository = build_repository()


@app.get("/health", response_model=HealthCheck)
@app.get("/healthz", response_model=HealthCheck, include_in_schema=False)
def health() -> HealthCheck:
    return HealthCheck()


@app.get("/api/stats", response_model=RepositoryStats)
def stats() -> RepositoryStats:
    return repository.stats()


@app.get("/api/entries", response_model=DiaryEntryList)
def list_entries(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> DiaryEntryList:
    entries, total = repository.list_entries(limit=limit, offset=offset)
    return DiaryEntryList(entries=entries, total=total, limit=limit, offset=offset)


@app.get("/api/entries/{entry_id}", response_model=DiaryEntry)
def get_entry(entry_id: str) -> DiaryEntry:
    entry = repository.get_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    return entry
