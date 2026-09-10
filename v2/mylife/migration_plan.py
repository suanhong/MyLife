from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass
from pathlib import Path

from .image_ids import legacy_image_id
from .legacy_refs import reference_aliases


@dataclass(frozen=True)
class PlannedImage:
    legacy_key: str
    image_id: str
    filename: str


@dataclass(frozen=True)
class PlannedDiary:
    legacy_key: str
    date: str
    text: str
    image_ids: tuple[str, ...]


def build_plan(path: str | Path) -> tuple[list[PlannedDiary], list[PlannedImage]]:
    """Build deterministic migration objects from a portable backup; no cloud writes."""
    with zipfile.ZipFile(path, "r") as archive:
        raw_images = json.loads(archive.read("images.json"))
        images = []
        alias_to_id = {}
        for item in raw_images:
            key = str(item.get("key", ""))
            image_id = legacy_image_id(key)
            images.append(PlannedImage(key, image_id, str(item.get("filename", ""))))
            aliases = set(reference_aliases(key))
            for field in ("filename", "original_size_key", "serving_size_key"):
                if item.get(field):
                    aliases.add(str(item[field]))
            for alias in aliases:
                previous = alias_to_id.get(alias)
                if previous and previous != image_id:
                    raise ValueError(f"ambiguous legacy image alias: {alias}")
                alias_to_id[alias] = image_id

        diaries = []
        for line in archive.read("diaries.jsonl").decode("utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            ids = []
            for ref in item.get("images") or []:
                candidates = {alias_to_id[a] for a in reference_aliases(str(ref)) if a in alias_to_id}
                if len(candidates) != 1:
                    raise ValueError(f"unresolved legacy image reference: {ref}")
                ids.append(candidates.pop())
            diaries.append(PlannedDiary(str(item.get("key", "")), str(item.get("date", "")),
                                         str(item.get("text") or ""), tuple(ids)))
    return diaries, images
