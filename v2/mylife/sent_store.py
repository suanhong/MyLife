from __future__ import annotations

from datetime import date

from google.cloud import datastore


class DatastoreSentStore:
    KIND = "V2DailyPrompt"

    def __init__(self, client: datastore.Client):
        self.client = client

    def _key(self, day: date):
        return self.client.key(self.KIND, day.isoformat())

    def was_sent(self, day: date) -> bool:
        entity = self.client.get(self._key(day))
        return bool(entity and entity.get("provider_message_id"))

    def mark_sent(self, day: date, provider_message_id: str) -> None:
        entity = datastore.Entity(key=self._key(day))
        entity.update({"date": day.isoformat(), "provider_message_id": provider_message_id})
        self.client.put(entity)


class DatastoreProcessedMessageStore:
    KIND = "V2ProcessedMessage"

    def __init__(self, client: datastore.Client):
        self.client = client

    def _key(self, message_id: str):
        return self.client.key(self.KIND, message_id)

    def contains(self, message_id: str) -> bool:
        return self.client.get(self._key(message_id)) is not None

    def mark_processed(self, message_id: str) -> None:
        entity = datastore.Entity(key=self._key(message_id))
        entity.update({"message_id": message_id})
        self.client.put(entity)
