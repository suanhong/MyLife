from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

from .repository import DiaryEntry


def write_backup(path: str | Path, entries: list[DiaryEntry]) -> str:
    """Create a disk-backed portable v2 backup and return its SHA-256."""
    path = Path(path)
    manifest = {"format": "MyLife v2 portable backup", "version": 1,
                "counts": {"posts": len(entries)}}
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as archive:
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        lines = []
        for entry in entries:
            lines.append(json.dumps({"date": entry.diary_date.isoformat(), "text": entry.text,
                                     "image_ids": list(entry.image_ids)}, ensure_ascii=False))
        archive.writestr("diaries.jsonl", "\n".join(lines) + ("\n" if lines else ""))
    with zipfile.ZipFile(path, "r") as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"backup CRC error: {bad}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
