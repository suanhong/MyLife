from __future__ import annotations

from datetime import date, datetime
from typing import Any

from google.cloud import datastore

from .models import DiaryEntry
from .storage import DiaryRepository


class DatastoreDiaryRepository(DiaryRepository):
    """Repository backed by Google Cloud Datastore/Firestore-in-Datastore mode.

    The importer will write v2 entities with kind `DiaryEntryV2`. This class is
    intentionally small so the FastAPI layer does not depend on Datastore types.
    """

    KIND = "DiaryEntryV2"

    def __init__(self, *, project_id: str | None = None, namespace: str | None = None) -> None:
        self.client = datastore.Client(project=project_id, namespace=namespace)

    def list_entries(self, *, limit: int, offset: int) -> tuple[list[DiaryEntry], int]:
        query = self.client.query(kind=self.KIND)
        query.order = ["-entry_date", "id"]
        entities = list(query.fetch(limit=limit, offset=offset, timeout=60))
        entries = [entity_to_diary_entry(entity) for entity in entities]

        # Datastore does not provide a cheap exact count in this client path.
        # Return the page count for now; replace with an aggregate/stat entity later.
        return entries, len(entries)

    def get_entry(self, entry_id: str) -> DiaryEntry | None:
        key = self.client.key(self.KIND, entry_id)
        entity = self.client.get(key)
        if entity is None:
            return None
        return entity_to_diary_entry(entity)


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
