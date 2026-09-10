from __future__ import annotations

from .image_magic import bytes_match_mime

MAX_IMAGE_BYTES = 20 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


def validate_image(content_type: str, data: bytes) -> None:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError("unsupported image MIME type")
    if not data:
        raise ValueError("empty image")
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("image exceeds size limit")
    if not bytes_match_mime(content_type, data):
        raise ValueError("image bytes do not match MIME type")
