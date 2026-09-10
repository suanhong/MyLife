from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass
class DiaryEntry:
    diary_date: date
    text: str
    image_ids: tuple[str, ...] = ()


class DiaryRepository(Protocol):
    def get(self, diary_date: date) -> DiaryEntry | None: ...
    def save(self, entry: DiaryEntry) -> None: ...
    def delete(self, diary_date: date) -> bool: ...


class MemoryDiaryRepository:
    """Small deterministic implementation for domain/API tests."""

    def __init__(self):
        self._entries: dict[date, DiaryEntry] = {}

    def get(self, diary_date: date) -> DiaryEntry | None:
        return self._entries.get(diary_date)

    def save(self, entry: DiaryEntry) -> None:
        self._entries[entry.diary_date] = entry

    def delete(self, diary_date: date) -> bool:
        return self._entries.pop(diary_date, None) is not None
