import json
import zipfile

from mylife.migration_plan import build_plan


def test_build_plan_maps_legacy_image_reference(tmp_path):
    path = tmp_path / "backup.zip"
    image = {"key": "Key('UserImage', 1)", "filename": "photo.jpg",
             "original_size_key": "photo.jpg", "serving_size_key": "photo-small.jpg"}
    post = {"key": "Key('Post', 1)", "date": "2026-09-10", "text": "hello",
            "images": ["Key('UserImage', 1)"]}
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("images.json", json.dumps([image]))
        archive.writestr("diaries.jsonl", json.dumps(post) + "\n")
    diaries, images = build_plan(path)
    assert len(diaries) == 1
    assert len(images) == 1
    assert diaries[0].image_ids == (images[0].image_id,)
