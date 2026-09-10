from __future__ import annotations

import secrets

from .image_metadata import ImageMetadata
from .image_validation import validate_image


def store_image(filename: str, content_type: str, data: bytes, object_store, metadata_repo):
    validate_image(content_type, data)
    image_id = secrets.token_urlsafe(18)
    stored = object_store.put(image_id, data, content_type)
    metadata = ImageMetadata(
        image_id=image_id,
        original_filename=filename,
        object_name=stored.object_name,
        content_type=stored.content_type,
        sha256=stored.sha256,
        size=stored.size,
    )
    metadata_repo.save(metadata)
    return metadata
