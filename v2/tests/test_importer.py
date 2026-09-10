import json
import zipfile

from mylife.importer import inspect_backup


def test_inspect_backup(tmp_path):
    path = tmp_path / "backup.zip"
    manifest = {"counts": {"posts": 2822, "user_images": 252, "image_references": 252}}
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("manifest.json", json.dumps(manifest))
        archive.writestr("diaries.jsonl", "{}\n")
        archive.writestr("images.json", "[]")

    summary = inspect_backup(path)
    assert summary.posts == 2822
    assert summary.images == 252
    assert summary.image_references == 252
