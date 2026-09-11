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
        # Keep this as a single-property order so the first read works without
        # requiring a composite Datastore index. Dates are ISO-8601 strings, so
        # descending lexical order is also descending chronological order.
        query.order = ["-entry_date"]
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
        entries = count_kind(self.client, self.DIARY_KIND)
        images = count_kind(self.client, self.IMAGE_KIND)

        # A projection query over a repeated property returns one projected row
        # per repeated value. Therefore each row contributes one image reference,
        # while entries-with-images must be de-duplicated by entity key.
        image_references = 0
        unique_refs: set[str] = set()
        entry_keys_with_images: set[str] = set()

        ref_query = self.client.query(kind=self.DIARY_KIND)
        ref_query.projection = ["image_refs"]
        for entity in ref_query.fetch(timeout=120):
            refs = normalize_refs(entity.get("image_refs"))
            if not refs:
                continue
            entry_keys_with_images.add(entity_key_id(entity))
            image_references += len(refs)
            unique_refs.update(refs)

        return RepositoryStats(
            entries=entries,
            images=images,
            image_references=image_references,
            unique_image_references=len(unique_refs),
            entries_with_images=len(entry_keys_with_images),
        )


def count_kind(client: datastore.Client, kind: str) -> int:
    query = client.query(kind=kind)
    query.keys_only()
    return sum(1 for _ in query.fetch(timeout=120))


def normalize_refs(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    return [str(value)]


def entity_key_id(entity: datastore.Entity) -> str:
    key = entity.key
    return key.name or str(key.id) or str(key)


def entity_to_diary_entry(entity: datastore.Entity) -> DiaryEntry:
    return DiaryEntry(
        id=str(entity.get("id") or entity.key.name or entity.key.id),
        entry_date=parse_date(entity.get("entry_date")),
        text=entity.get("text") or "",
        source=entity.get("source"),
        created_at=parse_datetime(entity.get("created_at")),
        updated_at=parse_datetime(entity.get("updated_at")),
        image_refs=normalize_refs(entity.get("image_refs")),
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
