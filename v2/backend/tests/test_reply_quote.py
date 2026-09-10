from app.reply_quote import strip_quoted_text


def test_strip_standard_quote():
    assert strip_quoted_text("new entry\n\nOn Thu, Sep 10, 2026 someone wrote:\n> prompt") == "new entry"
