class MemoryProcessedMessages:
    def __init__(self):
        self.ids = set()

    def claim(self, message_id: str | None) -> bool:
        if not message_id:
            return True
        if message_id in self.ids:
            return False
        self.ids.add(message_id)
        return True
