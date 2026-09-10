from datetime import date

from mylife.repository import DiaryEntry, MemoryDiaryRepository


def test_save_get_delete_entry():
    repo = MemoryDiaryRepository()
    entry = DiaryEntry(date(2026, 9, 10), "entry", ("img-1",))

    repo.save(entry)
    assert repo.get(entry.diary_date) == entry
    assert repo.delete(entry.diary_date)
    assert repo.get(entry.diary_date) is None
    assert not repo.delete(entry.diary_date)
