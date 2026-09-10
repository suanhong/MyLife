from __future__ import annotations

import re

_TOKEN = re.compile(r"\[MyLife:([A-Za-z0-9_-]+)\]")


def subject_with_token(subject: str, token: str) -> str:
    return f"{subject} [MyLife:{token}]"


def token_from_subject(subject: str) -> str | None:
    match = _TOKEN.search(subject or "")
    return match.group(1) if match else None
