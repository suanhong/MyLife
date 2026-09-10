from __future__ import annotations

from datetime import date

from .mailer import OutboundMessage, send_then_mark
from .old_post_service import find_old_entry
from .prompt import compose_prompt
from .reply_address import subject_with_token
from .reply_tokens import new_reply_token


def send_daily_prompt(day: date, recipient: str, repo, sent_store, mailer, token_store=None):
    if sent_store.was_sent(day):
        return None
    old = find_old_entry(day, repo)
    subject, text = compose_prompt(day, old)
    token = new_reply_token()
    if token_store is not None:
        token_store.save(token, day)
    message = OutboundMessage(recipient, subject_with_token(subject, token), text, token)

    def mark(receipt):
        sent_store.mark_sent(day, receipt.provider_message_id)

    return send_then_mark(message, mailer, mark)
