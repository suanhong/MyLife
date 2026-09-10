from __future__ import annotations

from email import policy
from email.parser import BytesParser

from .reply_address import token_from_subject


def resolve_reply_date(raw_message: bytes, token_store):
    message = BytesParser(policy=policy.default).parsebytes(raw_message, headersonly=True)
    token = token_from_subject(message.get("Subject", ""))
    return token_store.resolve(token) if token else None
