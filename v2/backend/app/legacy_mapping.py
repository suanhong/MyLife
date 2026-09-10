from __future__ import annotations

import re

KEY_RE = re.compile(r"Key\(['\"]UserImage['\"],\s*([^\)]+)\)")


def aliases(value: str) -> set[str]:
    raw = str(value).strip()
    result = {raw}
    match = KEY_RE.search(raw)
    if match:
        ident = match.group(1).strip().strip("'\"")
        result.update({ident, f"UserImage:{ident}", f"Key('UserImage', {ident})"})
    return result


def unresolved_image_refs(entries, images) -> list[str]:
    index = {}
    for image in images:
        values = set()
        if image.legacy_key:
            values.update(aliases(image.legacy_key))
        for value in (image.filename, image.storage_key):
            if value:
                values.add(value)
        for value in values:
            index.setdefault(value, set()).add(image.legacy_key or image.filename)
    unresolved = []
    for entry in entries:
        for ref in entry.image_refs:
            matches = set()
            for alias in aliases(ref):
                matches.update(index.get(alias, set()))
            if len(matches) != 1:
                unresolved.append(ref)
    return unresolved
