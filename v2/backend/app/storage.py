from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from .models import DiaryEntry, ImageRef, RepositoryStats


class DiaryRepository(ABC):
    @abstractmethod
    def list_entries(
        self,
        *,
        limit: int,
        offset: int,
        query_text: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> tuple[list[DiaryEntry], int]:
        raise NotImplementedError

    @abstractmethod
    def get_entry(self, entry_id: str) -> DiaryEntry | None:
        raise NotImplementedError

    @abstractmethod
    def get_image(self, image_ref: str) -> ImageRef | None:
        raise NotImplementedError

    @abstractmethod
    def stats(self) -> RepositoryStats:
        raise NotImplementedError


class InMemoryDiaryRepository(DiaryRepository):
    def __init__(self) -> None:
        self._entries: list[DiaryEntry] = [
            DiaryEntry(
                id="sample-1970-01-01",
                entry_date=date(1970, 1, 1),
                text="MyLife v2 backend is running.",
                source="system",
            )
        ]

    def list_entries(
        self,
        *,
        limit: int,
        offset: int,
        query_text: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> tuple[list[DiaryEntry], int]:
        entries = self._entries
        if date_from:
            entries = [entry for entry in entries if entry.entry_date >= date_from]
        if date_to:
            entries = [entry for entry in entries if entry.entry_date <= date_to]
        if query_text:
            needle = query_text.casefold()
            entries = [entry for entry in entries if needle in entry.text.casefold()]
        return entries[offset : offset + limit], len(entries)

    def get_entry(self, entry_id: str) -> DiaryEntry | None:
        return next((entry for entry in self._entries if entry.id == entry_id), None)

    def get_image(self, image_ref: str) -> ImageRef | None:
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
