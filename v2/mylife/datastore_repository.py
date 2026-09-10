from __future__ import annotations

from datetime import date

from google.cloud import datastore

from .repository import DiaryEntry


class DatastoreDiaryRepository:
    """v2 Datastore adapter using ISO diary dates as deterministic entity IDs."""

    KIND = "V2DiaryEntry"

    def __init__(self, client: datastore.Client):
        self.client = client

    def _key(self, diary_date: date):
        return self.client.key(self.KIND, diary_date.isoformat())

    def _entry(self, entity) -> DiaryEntry:
        return DiaryEntry(date.fromisoformat(entity["date"]), entity.get("text", ""),
                          tuple(entity.get("image_ids", [])))

    def get(self, diary_date: date) -> DiaryEntry | None:
        entity = self.client.get(self._key(diary_date))
        return self._entry(entity) if entity is not None else None

    def save(self, entry: DiaryEntry) -> None:
        entity = datastore.Entity(key=self._key(entry.diary_date), exclude_from_indexes=("text",))
        entity.update({"date": entry.diary_date.isoformat(), "text": entry.text,
                       "image_ids": list(entry.image_ids)})
        self.client.put(entity)

    def delete(self, diary_date: date) -> bool:
        key = self._key(diary_date)
        if self.client.get(key) is None:
            return False
        self.client.delete(key)
        return True

    def recent(self, limit: int = 30) -> list[DiaryEntry]:
        query = self.client.query(kind=self.KIND)
        query.order = ["-date"]
        return [self._entry(entity) for entity in query.fetch(limit=limit)]
