from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from .models import DiaryEntry, RepositoryStats


class DiaryRepository(ABC):
    @abstractmethod
    def list_entries(self, *, limit: int, offset: int) -> tuple[list[DiaryEntry], int]:
        raise NotImplementedError

    @abstractmethod
    def get_entry(self, entry_id: str) -> DiaryEntry | None:
        raise NotImplementedError

    @abstractmethod
    def stats(self) -> RepositoryStats:
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

    def stats(self) -> RepositoryStats:
        image_refs = [ref for entry in self._entries for ref in entry.image_refs]
        return RepositoryStats(
            entries=len(self._entries),
            images=0,
            image_references=len(image_refs),
            unique_image_references=len(set(image_refs)),
            entries_with_images=sum(1 for entry in self._entries if entry.image_refs),
        )
