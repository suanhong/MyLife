from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass
from pathlib import Path

from .legacy_refs import reference_aliases


@dataclass(frozen=True)
class MappingReport:
    posts: int
    image_entities: int
    references: int
    resolved: int
    unresolved: tuple[str, ...]


def _aliases(image: dict) -> set[str]:
    values = set()
    key = image.get("key")
    if key:
        values.update(reference_aliases(str(key)))
    for name in ("filename", "original_size_key", "serving_size_key"):
        value = image.get(name)
        if value:
            values.add(str(value))
    return values


def inspect_legacy_mapping(path: str | Path) -> MappingReport:
    """Resolve legacy Post.images references to UserImage records without writes."""
    with zipfile.ZipFile(path, "r") as archive:
        images = json.loads(archive.read("images.json"))
        alias_map = {}
        for image in images:
            for alias in _aliases(image):
                alias_map.setdefault(alias, []).append(image)

        posts = 0
        references = 0
        resolved = 0
        unresolved = []
        for line in archive.read("diaries.jsonl").decode("utf-8").splitlines():
            if not line.strip():
                continue
            posts += 1
            post = json.loads(line)
            for ref in post.get("images") or []:
                references += 1
                matches = []
                seen = set()
                for alias in reference_aliases(str(ref)):
                    for image in alias_map.get(alias, []):
                        marker = str(image.get("key", id(image)))
                        if marker not in seen:
                            seen.add(marker)
                            matches.append(image)
                if len(matches) == 1:
                    resolved += 1
                else:
                    unresolved.append(str(ref))

    return MappingReport(posts, len(images), references, resolved, tuple(unresolved))
