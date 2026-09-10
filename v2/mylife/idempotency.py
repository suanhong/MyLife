from __future__ import annotations

from typing import Protocol


class ProcessedMessageStore(Protocol):
    def contains(self, message_id: str) -> bool: ...
    def mark_processed(self, message_id: str) -> None: ...


class MemoryProcessedMessageStore:
    def __init__(self):
        self._ids: set[str] = set()

    def contains(self, message_id: str) -> bool:
        return message_id in self._ids

    def mark_processed(self, message_id: str) -> None:
        self._ids.add(message_id)


def accept_message_once(message_id: str | None, store: ProcessedMessageStore) -> bool:
    if not message_id:
        return True
    if store.contains(message_id):
        return False
    store.mark_processed(message_id)
    return True
