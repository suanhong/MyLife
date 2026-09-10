from mylife.reply_address import subject_with_token, token_from_subject


def test_reply_token_round_trip():
    subject = subject_with_token("MyLife diary", "abc_123-XYZ")
    assert token_from_subject(subject) == "abc_123-XYZ"
