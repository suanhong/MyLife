from datetime import date


class MemorySentStore:
    def __init__(self):
        self._sent: dict[date, str] = {}

    def was_sent(self, day: date) -> bool:
        return day in self._sent

    def mark_sent(self, day: date, provider_message_id: str) -> None:
        self._sent[day] = provider_message_id
