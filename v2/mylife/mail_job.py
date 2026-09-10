from __future__ import annotations

from .daily_service import send_daily_prompt
from .retry import retry


def run_daily_mail_job(day, recipient, repo, sent_store, mailer, token_store=None):
    return retry(lambda: send_daily_prompt(day, recipient, repo, sent_store, mailer, token_store),
                 attempts=3, base_delay=1.0)
