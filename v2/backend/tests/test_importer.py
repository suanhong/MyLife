from __future__ import annotations

import json
from pathlib import Path

from app.importer import load_diaries_jsonl, load_images_json, summarize_import


def test_load_diaries_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "diaries.jsonl"
    path.write_text(
        json.dumps({
            "key": "legacy-key-1",
            "date": "2020-01-02",
            "text": "hello",
            "source": "email",
            "created": "2020-01-02T03:04:05",
            "updated": "2020-01-02T04:05:06",
            "has_images": True,
            "images": ["ImageKey(1)", "ImageKey(2)"],
        }, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    entries = load_diaries_jsonl(path)

    assert len(entries) == 1
    assert entries[0].id == "legacy-000001-2020-01-02"
    assert entries[0].entry_date.isoformat() == "2020-01-02"
    assert entries[0].image_refs == ["ImageKey(1)", "ImageKey(2)"]
    assert entries[0].legacy_key == "legacy-key-1"


def test_load_images_json_with_manifest(tmp_path: Path) -> None:
    images_path = tmp_path / "images.json"
    manifest_path = tmp_path / "manifest.json"
    images_path.write_text(json.dumps([
        {"key": "ImageKey(1)", "filename": "a.jpg", "original_filename": "phone.jpg", "original_size_key": "a.jpg"}
    ]), encoding="utf-8")
    manifest_path.write_text(json.dumps({
        "photos": [{"filename": "a.jpg", "bytes": 123, "sha256": "abc"}]
    }), encoding="utf-8")

    images = load_images_json(images_path, manifest_path)

    assert len(images) == 1
    assert images[0].filename == "a.jpg"
    assert images[0].size_bytes == 123
    assert images[0].sha256 == "abc"


def test_summarize_import() -> None:
    entries = []
    images = []
    assert summarize_import(entries, images) == {
        "entries": 0,
        "images": 0,
        "image_references": 0,
        "unique_image_references": 0,
        "entries_with_images": 0,
    }
