from __future__ import annotations

import re

_KEY_PATTERNS = (
    re.compile(r"Key\(['\"]UserImage['\"],\s*([^\)]+)\)"),
    re.compile(r"<Key\(['\"]UserImage['\"],\s*([^\)]+)\)>"),
)


def reference_aliases(value: str) -> set[str]:
    """Return equivalent textual aliases for legacy UserImage key renderings."""
    raw = str(value).strip()
    aliases = {raw}
    for pattern in _KEY_PATTERNS:
        match = pattern.search(raw)
        if match:
            ident = match.group(1).strip().strip("'\"")
            aliases.update({ident, f"UserImage:{ident}", f"Key('UserImage', {ident})"})
    return aliases
