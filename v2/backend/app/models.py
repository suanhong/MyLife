from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class ImageRef(BaseModel):
    legacy_key: str | None = None
    filename: str
    original_filename: str | None = None
    content_type: str | None = None
    size_bytes: int | None = None
    sha256: str | None = None
    storage_key: str | None = None
    created_at: datetime | None = None


class DiaryEntry(BaseModel):
    id: str
    entry_date: date
    text: str = ""
    source: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    image_refs: list[str] = Field(default_factory=list)
    legacy_key: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DiaryEntryList(BaseModel):
    entries: list[DiaryEntry]
    total: int
    limit: int
    offset: int


class RepositoryStats(BaseModel):
    entries: int
    images: int
    image_references: int
    unique_image_references: int
    entries_with_images: int


class HealthCheck(BaseModel):
    status: str = "ok"
    service: str = "mylife-v2"
