class MemoryImageRepository:
    def __init__(self):
        self._values = {}

    def save(self, image):
        self._values[image.image_id] = image

    def get(self, image_id):
        return self._values.get(image_id)
