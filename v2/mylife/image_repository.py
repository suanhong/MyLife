from __future__ import annotations

from google.cloud import datastore

from .image_metadata import ImageMetadata


class DatastoreImageRepository:
    KIND = "V2Image"

    def __init__(self, client: datastore.Client):
        self.client = client

    def save(self, image: ImageMetadata) -> None:
        entity = datastore.Entity(key=self.client.key(self.KIND, image.image_id))
        entity.update({
            "original_filename": image.original_filename,
            "object_name": image.object_name,
            "content_type": image.content_type,
            "sha256": image.sha256,
            "size": image.size,
        })
        self.client.put(entity)

    def get(self, image_id: str) -> ImageMetadata | None:
        entity = self.client.get(self.client.key(self.KIND, image_id))
        if entity is None:
            return None
        return ImageMetadata(image_id, entity["original_filename"], entity["object_name"],
                             entity["content_type"], entity["sha256"], entity["size"])
