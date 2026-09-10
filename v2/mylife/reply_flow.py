from __future__ import annotations

from .reply_router import resolve_reply_date
from .service import ingest_reply


def process_inbound_reply(raw_message: bytes, token_store, repo, processed_store,
                          object_store=None, image_repo=None) -> bool:
    diary_date = resolve_reply_date(raw_message, token_store)
    if diary_date is None:
        return False
    return ingest_reply(raw_message, diary_date, repo, processed_store, object_store, image_repo)
