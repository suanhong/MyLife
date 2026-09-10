from datetime import date
from email.message import EmailMessage

from mylife.idempotency import MemoryProcessedMessageStore
from mylife.memory_image_repository import MemoryImageRepository
from mylife.memory_image_store import MemoryImageStore
from mylife.memory_reply_token_store import MemoryReplyTokenStore
from mylife.reply_flow import process_inbound_reply
from mylife.repository import MemoryDiaryRepository


def test_routed_reply_stores_image():
    tokens = MemoryReplyTokenStore()
    tokens.save("abc", date(2026, 9, 10))
    message = EmailMessage()
    message["Message-ID"] = "<img@example.com>"
    message["Subject"] = "Re: Diary [MyLife:abc]"
    message.set_content("entry")
    message.add_attachment(b"\xff\xd8\xffdata", maintype="image", subtype="jpeg", filename="photo.jpg")
    repo = MemoryDiaryRepository()
    assert process_inbound_reply(message.as_bytes(), tokens, repo, MemoryProcessedMessageStore(),
                                 MemoryImageStore(), MemoryImageRepository())
    assert len(repo.get(date(2026, 9, 10)).image_ids) == 1
