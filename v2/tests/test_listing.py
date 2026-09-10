from datetime import date

from mylife.repository import DiaryEntry, MemoryDiaryRepository


def test_recent_entries_newest_first():
    repo = MemoryDiaryRepository()
    repo.save(DiaryEntry(date(2026, 9, 8), "old"))
    repo.save(DiaryEntry(date(2026, 9, 10), "new"))
    assert [entry.text for entry in repo.recent(2)] == ["new", "old"]
