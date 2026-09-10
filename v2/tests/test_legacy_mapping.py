import json
import zipfile

from mylife.legacy_mapping import inspect_legacy_mapping


def test_legacy_reference_resolves_by_image_key(tmp_path):
    path = tmp_path / "backup.zip"
    image = {"key": "Key('UserImage', 1)", "filename": "photo.jpg",
             "original_size_key": "photo.jpg", "serving_size_key": "photo-small.jpg"}
    post = {"date": "2026-09-10", "images": ["Key('UserImage', 1)"]}
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("images.json", json.dumps([image]))
        archive.writestr("diaries.jsonl", json.dumps(post) + "\n")
    report = inspect_legacy_mapping(path)
    assert report.posts == 1
    assert report.references == 1
    assert report.resolved == 1
    assert report.unresolved == ()
