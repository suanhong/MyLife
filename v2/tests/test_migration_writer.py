import pytest

from mylife.migration_plan import PlannedDiary
from mylife.migration_writer import write_diaries
from mylife.repository import MemoryDiaryRepository


def test_migration_write_is_disabled_by_default():
    with pytest.raises(PermissionError):
        write_diaries([PlannedDiary("key", "2026-09-10", "text", ())], MemoryDiaryRepository())


def test_explicit_write_imports_diary():
    repo = MemoryDiaryRepository()
    count = write_diaries([PlannedDiary("key", "2026-09-10", "text", ())], repo, allow_writes=True)
    assert count == 1
    assert repo.recent(1)[0].text == "text"
