import zipfile
from datetime import date

from app.exporter import write_entries_zip
from app.models import DiaryEntry


def test_export_is_valid_zip(tmp_path):
    path = tmp_path / "export.zip"
    entry = DiaryEntry(id="1", entry_date=date(2026, 9, 10), text="hello")
    digest = write_entries_zip(path, [entry])
    assert len(digest) == 64
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
