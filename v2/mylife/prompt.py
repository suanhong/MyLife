from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class OldEntry:
    diary_date: date
    text: str


def compose_prompt(today: date, old_entry: OldEntry | None = None) -> tuple[str, str]:
    subject = f"MyLife diary - {today.isoformat()}"
    lines = [f"Write your diary for {today.isoformat()} by replying to this email."]
    if old_entry is not None:
        lines.extend(["", f"On this day: {old_entry.diary_date.isoformat()}", "", old_entry.text])
    return subject, "\n".join(lines)
