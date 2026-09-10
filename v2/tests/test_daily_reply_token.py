from datetime import date

from mylife.daily_service import send_daily_prompt
from mylife.mailer import SendReceipt
from mylife.memory_reply_token_store import MemoryReplyTokenStore
from mylife.memory_sent_store import MemorySentStore
from mylife.reply_address import token_from_subject
from mylife.repository import MemoryDiaryRepository


class CapturingMailer:
    def __init__(self): self.message = None
    def send(self, message):
        self.message = message
        return SendReceipt("provider")


def test_daily_prompt_token_routes_back_to_day():
    day = date(2026, 9, 10)
    tokens = MemoryReplyTokenStore()
    mailer = CapturingMailer()
    send_daily_prompt(day, "me@example.com", MemoryDiaryRepository(), MemorySentStore(), mailer, tokens)
    token = token_from_subject(mailer.message.subject)
    assert token
    assert tokens.resolve(token) == day
