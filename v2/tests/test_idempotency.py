from mylife.idempotency import MemoryProcessedMessageStore, accept_message_once


def test_message_id_is_accepted_only_once():
    store = MemoryProcessedMessageStore()
    assert accept_message_once("<message-1@example.com>", store)
    assert not accept_message_once("<message-1@example.com>", store)


def test_missing_message_id_can_be_processed():
    assert accept_message_once(None, MemoryProcessedMessageStore())
