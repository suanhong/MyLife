from datetime import date

import pytest

from mylife.daily_service import send_daily_prompt
from mylife.mailer import SendReceipt
from mylife.repository import MemoryDiaryRepository


class SentStore:
    def __init__(self): self.message_id = None
    def was_sent(self, day): return self.message_id is not None
    def mark_sent(self, day, provider_message_id): self.message_id = provider_message_id


class Mailer:
    def send(self, message): return SendReceipt("provider-id")


class FailingMailer:
    def send(self, message): raise RuntimeError("temporary failure")


def test_daily_prompt_marks_only_after_success():
    store = SentStore()
    send_daily_prompt(date(2026, 9, 10), "me@example.com", MemoryDiaryRepository(), store, Mailer())
    assert store.message_id == "provider-id"


def test_failure_leaves_day_retryable():
    store = SentStore()
    with pytest.raises(RuntimeError):
        send_daily_prompt(date(2026, 9, 10), "me@example.com", MemoryDiaryRepository(), store, FailingMailer())
    assert store.message_id is None
