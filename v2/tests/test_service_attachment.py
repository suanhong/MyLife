from datetime import date
from email.message import EmailMessage

from mylife.idempotency import MemoryProcessedMessageStore
from mylife.memory_image_repository import MemoryImageRepository
from mylife.memory_image_store import MemoryImageStore
from mylife.repository import MemoryDiaryRepository
from mylife.service import ingest_reply


def test_reply_image_is_linked_to_diary():
    message = EmailMessage()
    message["Message-ID"] = "<image-reply@example.com>"
    message.set_content("entry")
    message.add_attachment(b"\xff\xd8\xffdata", maintype="image", subtype="jpeg", filename="photo.jpg")
    repo = MemoryDiaryRepository()
    assert ingest_reply(message.as_bytes(), date(2026, 9, 10), repo,
                        MemoryProcessedMessageStore(), MemoryImageStore(), MemoryImageRepository())
    assert len(repo.get(date(2026, 9, 10)).image_ids) == 1
