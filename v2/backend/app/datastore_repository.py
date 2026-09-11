from __future__ import annotations

from datetime import date, datetime
from typing import Any

from google.cloud import datastore

from .models import DiaryEntry, RepositoryStats
from .storage import DiaryRepository


class DatastoreDiaryRepository(DiaryRepository):
    """Repository backed by Google Cloud Datastore/Firestore-in-Datastore mode.

    The importer writes v2 entities with kinds `DiaryEntryV2` and `ImageRefV2`.
    This class is intentionally small so the FastAPI layer does not depend on
    Datastore types.
    """

    DIARY_KIND = "DiaryEntryV2"
    IMAGE_KIND = "ImageRefV2"

    def __init__(self, *, project_id: str | None = None, namespace: str | None = None) -> None:
        self.client = datastore.Client(project=project_id, namespace=namespace)

    def list_entries(self, *, limit: int, offset: int) -> tuple[list[DiaryEntry], int]:
        query = self.client.query(kind=self.DIARY_KIND)
        query.order = ["-entry_date", "id"]
        entities = list(query.fetch(limit=limit, offset=offset, timeout=60))
        entries = [entity_to_diary_entry(entity) for entity in entities]

        # Datastore does not provide a cheap exact count in this client path.
        # Return the page count for now; replace with an aggregate/stat entity later.
        return entries, len(entries)

    def get_entry(self, entry_id: str) -> DiaryEntry | None:
        key = self.client.key(self.DIARY_KIND, entry_id)
        entity = self.client.get(key)
        if entity is None:
            return None
        return entity_to_diary_entry(entity)

    def stats(self) -> RepositoryStats:
        entries = 0
        image_references = 0
        unique_refs: set[str] = set()
        entries_with_images = 0

        diary_query = self.client.query(kind=self.DIARY_KIND)
        diary_query.keys_only()
        for entity in diary_query.fetch(timeout=120):
            entries += 1

        ref_query = self.client.query(kind=self.DIARY_KIND)
        ref_query.projection = ["image_refs"]
        for entity in ref_query.fetch(timeout=120):
            refs = list(entity.get("image_refs") or [])
            if refs:
                entries_with_images += 1
            image_references += len(refs)
            unique_refs.update(str(ref) for ref in refs)

        image_query = self.client.query(kind=self.IMAGE_KIND)
        image_query.keys_only()
        images = sum(1 for _ in image_query.fetch(timeout=120))

        return RepositoryStats(
            entries=entries,
            images=images,
            image_references=image_references,
            unique_image_references=len(unique_refs),
            entries_with_images=entries_with_images,
        )


def entity_to_diary_entry(entity: datastore.Entity) -> DiaryEntry:
    return DiaryEntry(
        id=str(entity.get("id") or entity.key.name or entity.key.id),
        entry_date=parse_date(entity.get("entry_date")),
        text=entity.get("text") or "",
        source=entity.get("source"),
        created_at=parse_datetime(entity.get("created_at")),
        updated_at=parse_datetime(entity.get("updated_at")),
        image_refs=list(entity.get("image_refs") or []),
        legacy_key=entity.get("legacy_key"),
        metadata=dict(entity.get("metadata") or {}),
    )


def parse_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value[:10])
    raise ValueError(f"Cannot parse date from Datastore value: {value!r}")


def parse_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None
