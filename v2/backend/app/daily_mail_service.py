from __future__ import annotations

from .daily_prompt import compose_daily_prompt
from .mail_domain import subject_with_token
from .mail_send_state import send_then_mark
from .mail_types import OutboundMail
from .reply_tokens import new_reply_token


def send_daily(day, recipient, old_entry, sent_store, token_store, mailer):
    if sent_store.was_sent(day):
        return None
    token = new_reply_token()
    token_store.save(token, day)
    old_date = getattr(old_entry, "entry_date", None) if old_entry else None
    old_text = getattr(old_entry, "text", None) if old_entry else None
    subject, body = compose_daily_prompt(day, old_date, old_text)
    message = OutboundMail(recipient, subject_with_token(subject, token), body)

    def mark(receipt):
        sent_store.mark_sent(day, receipt.provider_message_id)

    return send_then_mark(message, mailer, mark)
