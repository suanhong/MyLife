from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from .models import DiaryEntry, DiaryEntryList, HealthCheck
from .storage import DiaryRepository, InMemoryDiaryRepository

app = FastAPI(
    title="MyLife v2",
    version="0.1.0",
    description="Modern replacement for the legacy MyLife diary service.",
)

repository: DiaryRepository = InMemoryDiaryRepository()


@app.get("/healthz", response_model=HealthCheck)
def healthz() -> HealthCheck:
    return HealthCheck()


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
