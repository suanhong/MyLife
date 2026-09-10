from __future__ import annotations

from datetime import date

from .idempotency import ProcessedMessageStore, accept_message_once
from .mail import parse_reply
from .quote_strip import strip_quoted_reply
from .repository import DiaryEntry, DiaryRepository


def ingest_reply(raw_message: bytes, diary_date: date, repo: DiaryRepository,
                 processed: ProcessedMessageStore) -> bool:
    parsed = parse_reply(raw_message)
    if not accept_message_once(parsed.message_id, processed):
        return False
    body = parsed.plain_text if parsed.plain_text is not None else (parsed.html_text or "")
    body = strip_quoted_reply(body) if parsed.plain_text is not None else body.strip()
    existing = repo.get(diary_date)
    image_ids = existing.image_ids if existing else ()
    repo.save(DiaryEntry(diary_date, body, image_ids))
    return True
