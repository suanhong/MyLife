from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from .models import DiaryEntry


class DiaryRepository(ABC):
    @abstractmethod
    def list_entries(self, *, limit: int, offset: int) -> tuple[list[DiaryEntry], int]:
        raise NotImplementedError

    @abstractmethod
    def get_entry(self, entry_id: str) -> DiaryEntry | None:
        raise NotImplementedError


class InMemoryDiaryRepository(DiaryRepository):
    """Development placeholder until the importer/storage layer is wired."""

    def __init__(self) -> None:
        self._entries: list[DiaryEntry] = [
            DiaryEntry(
                id="sample-1970-01-01",
                entry_date=date(1970, 1, 1),
                text="MyLife v2 backend is running.",
                source="system",
            )
        ]

    def list_entries(self, *, limit: int, offset: int) -> tuple[list[DiaryEntry], int]:
        return self._entries[offset : offset + limit], len(self._entries)

    def get_entry(self, entry_id: str) -> DiaryEntry | None:
        for entry in self._entries:
            if entry.id == entry_id:
                return entry
        return None
