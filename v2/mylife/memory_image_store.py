import hashlib

from .image_store import StoredImage


class MemoryImageStore:
    def __init__(self):
        self._objects = {}

    def put(self, image_id, data, content_type):
        object_name = f"v2/images/{image_id}/original"
        self._objects[object_name] = data
        return StoredImage(image_id, object_name, content_type, hashlib.sha256(data).hexdigest(), len(data))

    def read(self, object_name):
        return self._objects[object_name]

    def delete(self, object_name):
        self._objects.pop(object_name, None)
