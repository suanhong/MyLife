from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass
from pathlib import Path

from .importer import BackupSummary, inspect_backup


@dataclass(frozen=True)
class PortableEntry:
    key: str
    date: str
    text: str
    image_refs: tuple[str, ...]


def load_entries(path: str | Path) -> tuple[BackupSummary, list[PortableEntry]]:
    """Read and cross-check diary records from a verified portable backup.

    This function performs no Datastore or Cloud Storage writes.
    """
    summary = inspect_backup(path)
    entries = []
    with zipfile.ZipFile(path, "r") as archive:
        raw = archive.read("diaries.jsonl").decode("utf-8")
        for line_no, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                continue
            item = json.loads(line)
            entries.append(PortableEntry(
                key=str(item.get("key", "")),
                date=str(item.get("date", "")),
                text=str(item.get("text") or ""),
                image_refs=tuple(str(v) for v in (item.get("images") or [])),
            ))
    if len(entries) != summary.posts:
        raise ValueError(f"manifest says {summary.posts} posts but JSONL contains {len(entries)}")
    if sum(len(entry.image_refs) for entry in entries) != summary.image_references:
        raise ValueError("image reference count does not match manifest")
    return summary, entries
