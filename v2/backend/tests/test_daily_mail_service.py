from datetime import date

import pytest

from app.daily_mail_service import send_daily
from app.mail_types import MailReceipt


class Sent:
    def __init__(self): self.value = None
    def was_sent(self, day): return self.value is not None
    def mark_sent(self, day, value): self.value = value


class Tokens:
    def save(self, token, day): self.day = day


class Good:
    def send(self, message): return MailReceipt("provider")


class Bad:
    def send(self, message): raise RuntimeError("temporary")


def test_success_marks_sent():
    sent = Sent()
    send_daily(date(2026, 9, 10), "me@example.com", None, sent, Tokens(), Good())
    assert sent.value == "provider"


def test_failure_remains_retryable():
    sent = Sent()
    with pytest.raises(RuntimeError):
        send_daily(date(2026, 9, 10), "me@example.com", None, sent, Tokens(), Bad())
    assert sent.value is None
