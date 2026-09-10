from datetime import date

from mylife.export_service import export_recent
from mylife.repository import DiaryEntry, MemoryDiaryRepository


def test_export_recent_creates_backup(tmp_path):
    repo = MemoryDiaryRepository()
    repo.save(DiaryEntry(date(2026, 9, 10), "entry"))
    path = tmp_path / "export.zip"
    digest = export_recent(repo, path)
    assert path.exists()
    assert len(digest) == 64
