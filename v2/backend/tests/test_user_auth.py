from app.user_auth import user_allowed


def test_only_owner_email_is_allowed():
    assert user_allowed("Me@Example.com", "me@example.com")
    assert not user_allowed("other@example.com", "me@example.com")
