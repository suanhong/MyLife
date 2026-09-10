from datetime import date
from email.message import EmailMessage

from mylife.memory_reply_token_store import MemoryReplyTokenStore
from mylife.reply_router import resolve_reply_date


def test_subject_token_resolves_diary_date():
    store = MemoryReplyTokenStore()
    store.save("abc", date(2026, 9, 10))
    message = EmailMessage()
    message["Subject"] = "Re: MyLife diary [MyLife:abc]"
    message.set_content("entry")
    assert resolve_reply_date(message.as_bytes(), store) == date(2026, 9, 10)
