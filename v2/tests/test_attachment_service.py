from mylife.attachment_service import store_reply_images
from mylife.mail import Attachment, ParsedReply
from mylife.memory_image_repository import MemoryImageRepository
from mylife.memory_image_store import MemoryImageStore


def test_reply_image_is_stored():
    parsed = ParsedReply("<id>", "entry", None, (
        Attachment("photo.jpg", "image/jpeg", None, b"\xff\xd8\xffdata"),
    ))
    metadata = MemoryImageRepository()
    stored = store_reply_images(parsed, MemoryImageStore(), metadata)
    assert len(stored) == 1
    assert metadata.get(stored[0].image_id) == stored[0]
