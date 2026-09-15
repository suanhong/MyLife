from __future__ import annotations

from datetime import date, datetime
from typing import Any

from google.cloud import datastore
from google.cloud.datastore.query import PropertyFilter

from .models import DiaryEntry, ImageRef, RepositoryStats
from .storage import DiaryRepository


class DatastoreDiaryRepository(DiaryRepository):
    DIARY_KIND = "DiaryEntryV2"
    IMAGE_KIND = "ImageRefV2"

    def __init__(self, *, project_id: str | None = None, namespace: str | None = None) -> None:
        self.client = datastore.Client(project=project_id, namespace=namespace)

    def list_entries(
        self,
        *,
        limit: int,
        offset: int,
        query_text: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> tuple[list[DiaryEntry], int]:
        query = self.client.query(kind=self.DIARY_KIND)
        if date_from:
            query.add_filter(filter=PropertyFilter("entry_date", ">=", date_from.isoformat()))
        if date_to:
            query.add_filter(filter=PropertyFilter("entry_date", "<=", date_to.isoformat()))
        query.order = ["-entry_date"]

        if query_text:
            # Datastore has no native full-text index. The personal corpus is
            # deliberately scanned only when the user submits a text search.
            needle = query_text.casefold()
            matches = [
                entity_to_diary_entry(entity)
                for entity in query.fetch(timeout=120)
                if needle in str(entity.get("text") or "").casefold()
            ]
            return matches[offset : offset + limit], len(matches)

        entities = list(query.fetch(limit=limit, offset=offset, timeout=60))
        entries = [entity_to_diary_entry(entity) for entity in entities]
        return entries, count_query(self.client, query)

    def get_entry(self, entry_id: str) -> DiaryEntry | None:
        entity = self.client.get(self.client.key(self.DIARY_KIND, entry_id))
        return entity_to_diary_entry(entity) if entity is not None else None

    def get_image(self, image_ref: str) -> ImageRef | None:
        entity = self.client.get(self.client.key(self.IMAGE_KIND, image_ref))
        return entity_to_image_ref(entity) if entity is not None else None

    def stats(self) -> RepositoryStats:
        entries = count_kind(self.client, self.DIARY_KIND)
        images = count_kind(self.client, self.IMAGE_KIND)
        image_references = 0
        unique_refs: set[str] = set()
        entry_keys_with_images: set[str] = set()

        ref_query = self.client.query(kind=self.DIARY_KIND)
        ref_query.projection = ["image_refs"]
        for entity in ref_query.fetch(timeout=120):
            refs = normalize_refs(entity.get("image_refs"))
            if refs:
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


def count_query(client: datastore.Client, query: Any) -> int:
    aggregation = client.aggregation_query(query)
    aggregation.count(alias="total")
    rows = list(aggregation.fetch(timeout=120))
    if not rows or not rows[0]:
        return 0
    return int(rows[0][0].value)


def count_kind(client: datastore.Client, kind: str) -> int:
    return count_query(client, client.query(kind=kind))


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


def entity_to_image_ref(entity: datastore.Entity) -> ImageRef:
    return ImageRef(
        legacy_key=entity.get("legacy_key"),
        filename=str(entity.get("filename") or ""),
        original_filename=entity.get("original_filename"),
        content_type=entity.get("content_type"),
        size_bytes=entity.get("size_bytes"),
        sha256=entity.get("sha256"),
        storage_key=entity.get("storage_key"),
        created_at=parse_datetime(entity.get("created_at")),
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
