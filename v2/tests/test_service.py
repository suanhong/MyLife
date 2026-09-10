from datetime import date
from email.message import EmailMessage

from mylife.idempotency import MemoryProcessedMessageStore
from mylife.repository import MemoryDiaryRepository
from mylife.service import ingest_reply


def raw_reply(message_id="<one@example.com>"):
    message = EmailMessage()
    message["Message-ID"] = message_id
    message.set_content("My new diary\n\nOn Thu, Sep 10, 2026 someone wrote:\n> old prompt")
    return message.as_bytes()


def test_reply_creates_diary_and_duplicate_is_ignored():
    repo = MemoryDiaryRepository()
    processed = MemoryProcessedMessageStore()
    day = date(2026, 9, 10)

    assert ingest_reply(raw_reply(), day, repo, processed)
    assert repo.get(day).text == "My new diary"
    assert not ingest_reply(raw_reply(), day, repo, processed)
