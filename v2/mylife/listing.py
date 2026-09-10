from __future__ import annotations

from datetime import date
from typing import Protocol

from .repository import DiaryEntry


class DiaryListingRepository(Protocol):
    def recent(self, limit: int = 30) -> list[DiaryEntry]: ...


def recent_entries(repo: DiaryListingRepository, limit: int = 30) -> list[DiaryEntry]:
    if limit < 1 or limit > 365:
        raise ValueError("limit must be between 1 and 365")
    return repo.recent(limit)
