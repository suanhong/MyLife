from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageMetadata:
    image_id: str
    original_filename: str
    object_name: str
    content_type: str
    sha256: str
    size: int
