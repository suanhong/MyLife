from __future__ import annotations

from typing import Protocol


class Thumbnailer(Protocol):
    def make(self, data: bytes, content_type: str, max_size: int = 500) -> bytes: ...


def thumbnail_object_name(image_id: str) -> str:
    return f"v2/images/{image_id}/thumbnail"
