from mylife.image_metadata import ImageMetadata
from mylife.image_service import store_image
from mylife.image_store import StoredImage


class ObjectStore:
    def put(self, image_id, data, content_type):
        return StoredImage(image_id, f"v2/images/{image_id}/original", content_type, "hash", len(data))


class MetadataRepo:
    def __init__(self): self.value = None
    def save(self, value): self.value = value


def test_store_valid_image_records_metadata():
    repo = MetadataRepo()
    result = store_image("photo.jpg", "image/jpeg", b"\xff\xd8\xffdata", ObjectStore(), repo)
    assert isinstance(result, ImageMetadata)
    assert repo.value == result
    assert result.original_filename == "photo.jpg"
