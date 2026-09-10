from __future__ import annotations

import re

REPLY_MARKERS = (
    re.compile(r"^On .+ wrote:$", re.IGNORECASE),
    re.compile(r"^[- ]*Original Message[- ]*$", re.IGNORECASE),
)


def strip_quoted_reply(text: str) -> str:
    """Keep newly typed plain text and stop at common quoted-message boundaries."""
    kept = []
    for line in text.splitlines():
        if line.startswith(">") or any(pattern.match(line.strip()) for pattern in REPLY_MARKERS):
            break
        kept.append(line)
    return "\n".join(kept).strip()
