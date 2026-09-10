from datetime import date


class MemoryReplyTokenStore:
    def __init__(self):
        self._values: dict[str, date] = {}

    def save(self, token: str, diary_date: date) -> None:
        self._values[token] = diary_date

    def resolve(self, token: str) -> date | None:
        return self._values.get(token)
