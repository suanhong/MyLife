from datetime import date

from mylife.old_post_service import find_old_entry
from mylife.repository import DiaryEntry, MemoryDiaryRepository


def test_nearest_anniversary_wins():
    repo = MemoryDiaryRepository()
    repo.save(DiaryEntry(date(2024, 9, 10), "two years"))
    repo.save(DiaryEntry(date(2023, 9, 10), "three years"))
    old = find_old_entry(date(2026, 9, 10), repo)
    assert old.diary_date == date(2024, 9, 10)
