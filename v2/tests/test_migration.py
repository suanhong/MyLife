import json
import zipfile

from mylife.migration import load_entries


def test_load_entries_cross_checks_manifest(tmp_path):
    path = tmp_path / "backup.zip"
    manifest = {"counts": {"posts": 1, "user_images": 0, "image_references": 0}}
    post = {"key": "Post:1", "date": "2026-09-10", "text": "hello", "images": []}
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("manifest.json", json.dumps(manifest))
        archive.writestr("images.json", "[]")
        archive.writestr("diaries.jsonl", json.dumps(post) + "\n")

    summary, entries = load_entries(path)
    assert summary.posts == 1
    assert entries[0].date == "2026-09-10"
    assert entries[0].text == "hello"
