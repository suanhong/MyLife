from __future__ import annotations

from datetime import date

from .old_posts import anniversary_candidates
from .prompt import OldEntry


def find_old_entry(today: date, repo, years: int = 10) -> OldEntry | None:
    for candidate in anniversary_candidates(today, years):
        entry = repo.get(candidate)
        if entry is not None:
            return OldEntry(entry.diary_date, entry.text)
    return None
