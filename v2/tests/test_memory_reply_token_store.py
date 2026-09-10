from datetime import date

from mylife.memory_reply_token_store import MemoryReplyTokenStore


def test_token_maps_to_diary_date():
    store = MemoryReplyTokenStore()
    day = date(2026, 9, 10)
    store.save("token", day)
    assert store.resolve("token") == day
