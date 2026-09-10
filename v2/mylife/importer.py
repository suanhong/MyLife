from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BackupSummary:
    posts: int
    images: int
    image_references: int


def inspect_backup(path: str | Path) -> BackupSummary:
    """Validate portable backup structure without writing application data."""
    with zipfile.ZipFile(path, "r") as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"backup CRC error: {bad}")
        names = set(archive.namelist())
        required = {"diaries.jsonl", "images.json", "manifest.json"}
        missing = required - names
        if missing:
            raise ValueError(f"backup missing required files: {sorted(missing)}")
        manifest = json.loads(archive.read("manifest.json"))
        counts = manifest.get("counts", {})
        return BackupSummary(
            posts=int(counts.get("posts", 0)),
            images=int(counts.get("user_images", 0)),
            image_references=int(counts.get("image_references", 0)),
        )
