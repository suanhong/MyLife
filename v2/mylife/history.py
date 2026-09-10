from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DiaryEvent:
    action: str
    diary_date: str
    occurred_at: datetime
    source: str
