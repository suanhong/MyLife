from __future__ import annotations

MAX_IMAGE_BYTES = 20 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


def validate_image(content_type: str, data: bytes) -> None:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError("unsupported image MIME type")
    if not data:
        raise ValueError("empty image")
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("image exceeds size limit")
