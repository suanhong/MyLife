from __future__ import annotations

from .image_service import store_image
from .mail import ParsedReply


def store_reply_images(parsed: ParsedReply, object_store, metadata_repo):
    stored = []
    for attachment in parsed.attachments:
        stored.append(store_image(
            attachment.filename,
            attachment.content_type,
            attachment.data,
            object_store,
            metadata_repo,
        ))
    return stored
