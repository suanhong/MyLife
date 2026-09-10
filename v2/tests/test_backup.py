import zipfile
from datetime import date

from mylife.backup import write_backup
from mylife.repository import DiaryEntry


def test_write_backup_has_valid_crc_and_hash(tmp_path):
    path = tmp_path / "backup.zip"
    digest = write_backup(path, [DiaryEntry(date(2026, 9, 10), "hello")])
    assert len(digest) == 64
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        assert {"manifest.json", "diaries.jsonl"} <= set(archive.namelist())
