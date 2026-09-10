from __future__ import annotations

import hashlib
from dataclasses import dataclass

from google.cloud import storage


@dataclass(frozen=True)
class StoredImage:
    image_id: str
    object_name: str
    content_type: str
    sha256: str
    size: int


class CloudStorageImageStore:
    """Private image object store. This adapter never makes objects public."""

    def __init__(self, client: storage.Client, bucket_name: str):
        self.bucket = client.bucket(bucket_name)

    def put(self, image_id: str, data: bytes, content_type: str) -> StoredImage:
        if not content_type.startswith("image/"):
            raise ValueError("only image MIME types are accepted")
        digest = hashlib.sha256(data).hexdigest()
        object_name = f"v2/images/{image_id}/original"
        blob = self.bucket.blob(object_name)
        blob.upload_from_string(data, content_type=content_type)
        return StoredImage(image_id, object_name, content_type, digest, len(data))

    def read(self, object_name: str) -> bytes:
        return self.bucket.blob(object_name).download_as_bytes()

    def delete(self, object_name: str) -> None:
        self.bucket.blob(object_name).delete()
