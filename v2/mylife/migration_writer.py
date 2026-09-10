from __future__ import annotations

from datetime import date

from .repository import DiaryEntry


def write_diaries(plan, repo, *, allow_writes: bool = False) -> int:
    """Write a validated migration plan only when explicitly enabled.

    This guard prevents accidental writes while running normal dry-run tooling.
    """
    if not allow_writes:
        raise PermissionError("migration writes are disabled")
    count = 0
    for item in plan:
        repo.save(DiaryEntry(date.fromisoformat(item.date), item.text, item.image_ids))
        count += 1
    return count
