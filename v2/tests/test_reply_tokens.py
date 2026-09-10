from mylife.reply_tokens import new_reply_token


def test_reply_tokens_are_unique_and_opaque():
    first = new_reply_token()
    second = new_reply_token()
    assert first != second
    assert len(first) >= 24
