from mylife.quote_strip import strip_quoted_reply


def test_stops_before_standard_quoted_reply():
    text = "New diary text\n\nOn Thu, Sep 10, 2026 someone wrote:\n> old prompt"
    assert strip_quoted_reply(text) == "New diary text"


def test_plain_multiline_text_is_preserved():
    assert strip_quoted_reply("line one\nline two") == "line one\nline two"
