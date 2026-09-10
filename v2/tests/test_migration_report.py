import json
import zipfile

from mylife.migration_report import migration_report


def test_report_marks_resolved_backup_ready(tmp_path):
    path = tmp_path / "backup.zip"
    image = {"key": "Key('UserImage', 1)", "filename": "a.jpg", "original_size_key": "a.jpg"}
    post = {"key": "Post:1", "date": "2026-09-10", "text": "x", "images": ["Key('UserImage', 1)"]}
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("images.json", json.dumps([image]))
        archive.writestr("diaries.jsonl", json.dumps(post) + "\n")
    report = migration_report(path)
    assert report["ready_for_staging_write"]
    assert report["planned_image_references"] == 1
