from __future__ import annotations

from datetime import date

from google.cloud import datastore


class DatastoreReplyTokenStore:
    KIND = "V2ReplyToken"

    def __init__(self, client: datastore.Client):
        self.client = client

    def save(self, token: str, diary_date: date) -> None:
        entity = datastore.Entity(key=self.client.key(self.KIND, token))
        entity.update({"date": diary_date.isoformat()})
        self.client.put(entity)

    def resolve(self, token: str) -> date | None:
        entity = self.client.get(self.client.key(self.KIND, token))
        return date.fromisoformat(entity["date"]) if entity else None
