MAX_IMAGE_BYTES = 20 * 1024 * 1024


def _matches(content_type: str, data: bytes) -> bool:
    if content_type == "image/jpeg": return data.startswith(b"\xff\xd8\xff")
    if content_type == "image/png": return data.startswith(b"\x89PNG\r\n\x1a\n")
    if content_type == "image/gif": return data.startswith((b"GIF87a", b"GIF89a"))
    if content_type == "image/webp": return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    return False


def validate_image(content_type: str, data: bytes) -> None:
    if not data:
        raise ValueError("empty image")
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("image exceeds size limit")
    if not _matches(content_type, data):
        raise ValueError("unsupported or mismatched image MIME type")
