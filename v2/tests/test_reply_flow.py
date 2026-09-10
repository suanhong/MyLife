from datetime import date
from email.message import EmailMessage

from mylife.idempotency import MemoryProcessedMessageStore
from mylife.memory_reply_token_store import MemoryReplyTokenStore
from mylife.reply_flow import process_inbound_reply
from mylife.repository import MemoryDiaryRepository


def test_inbound_reply_is_routed_and_saved():
    tokens = MemoryReplyTokenStore()
    tokens.save("abc", date(2026, 9, 10))
    message = EmailMessage()
    message["Message-ID"] = "<reply@example.com>"
    message["Subject"] = "Re: Diary [MyLife:abc]"
    message.set_content("today's entry")
    repo = MemoryDiaryRepository()
    assert process_inbound_reply(message.as_bytes(), tokens, repo, MemoryProcessedMessageStore())
    assert repo.get(date(2026, 9, 10)).text == "today's entry"
