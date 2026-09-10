from app.reply_idempotency import MemoryProcessedMessages


def test_message_id_claimed_once():
    store = MemoryProcessedMessages()
    assert store.claim("<id@example.com>")
    assert not store.claim("<id@example.com>")
