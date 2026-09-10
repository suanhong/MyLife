from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

from .models import DiaryEntry, ImageRef


def parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


def parse_date(value: Any) -> date:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            pass
    raise ValueError(f"Cannot parse diary date: {value!r}")


def stable_entry_id(index: int, raw: dict[str, Any]) -> str:
    entry_date = str(raw.get("date") or "unknown")[:10]
    return f"legacy-{index:06d}-{entry_date}"


def load_diaries_jsonl(path: Path) -> list[DiaryEntry]:
    entries: list[DiaryEntry] = []
    with path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle, 1):
            if not line.strip():
                continue
            raw = json.loads(line)
            entries.append(
                DiaryEntry(
                    id=stable_entry_id(index, raw),
                    entry_date=parse_date(raw.get("date")),
                    text=raw.get("text") or "",
                    source=raw.get("source"),
                    created_at=parse_datetime(raw.get("created")),
                    updated_at=parse_datetime(raw.get("updated")),
                    image_refs=list(raw.get("images") or []),
                    legacy_key=raw.get("key"),
                    metadata={
                        "legacy_has_images": raw.get("has_images"),
                    },
                )
            )
    return entries


def load_images_json(path: Path, manifest_path: Path | None = None) -> list[ImageRef]:
    sha_by_filename: dict[str, dict[str, Any]] = {}
    if manifest_path and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for item in manifest.get("photos", []):
            sha_by_filename[item.get("filename")] = item

    raw_images = json.loads(path.read_text(encoding="utf-8"))
    images: list[ImageRef] = []
    for raw in raw_images:
        filename = raw.get("filename")
        if not filename:
            continue
        photo = sha_by_filename.get(filename, {})
        images.append(
            ImageRef(
                legacy_key=raw.get("key"),
                filename=filename,
                original_filename=raw.get("original_filename"),
                size_bytes=photo.get("bytes"),
                sha256=photo.get("sha256"),
                storage_key=raw.get("original_size_key"),
                created_at=parse_datetime(raw.get("created")),
            )
        )
    return images


def summarize_import(entries: Iterable[DiaryEntry], images: Iterable[ImageRef]) -> dict[str, int]:
    entry_list = list(entries)
    image_list = list(images)
    refs = [ref for entry in entry_list for ref in entry.image_refs]
    return {
        "entries": len(entry_list),
        "images": len(image_list),
        "image_references": len(refs),
        "unique_image_references": len(set(refs)),
        "entries_with_images": sum(1 for entry in entry_list if entry.image_refs),
    }
