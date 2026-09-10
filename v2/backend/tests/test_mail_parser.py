from email.message import EmailMessage

from app.mail_parser import parse_reply


def test_parse_reply_with_image():
    message = EmailMessage()
    message["Message-ID"] = "<id@example.com>"
    message["Subject"] = "Re: Diary [MyLife:abc]"
    message.set_content("entry")
    message.add_attachment(b"\xff\xd8\xffdata", maintype="image", subtype="jpeg", filename="photo.jpg")
    parsed = parse_reply(message.as_bytes())
    assert parsed.message_id == "<id@example.com>"
    assert "entry" in parsed.plain_text
    assert len(parsed.attachments) == 1
    assert parsed.attachments[0].filename == "photo.jpg"
