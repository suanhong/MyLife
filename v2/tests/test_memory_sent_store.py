from datetime import date

from mylife.memory_sent_store import MemorySentStore


def test_sent_state():
    store = MemorySentStore()
    day = date(2026, 9, 10)
    assert not store.was_sent(day)
    store.mark_sent(day, "provider")
    assert store.was_sent(day)
