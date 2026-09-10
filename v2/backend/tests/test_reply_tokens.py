from app.reply_tokens import new_reply_token


def test_tokens_are_unique():
    assert new_reply_token() != new_reply_token()
