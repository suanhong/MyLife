from email.message import EmailMessage

from mylife.mail import parse_reply


def test_parse_plain_reply_and_image_attachment():
    message = EmailMessage()
    message["Message-ID"] = "<abc@example.com>"
    message.set_content("Today was a good day.")
    message.add_attachment(b"jpeg-bytes", maintype="image", subtype="jpeg", filename="photo.jpg")

    parsed = parse_reply(message.as_bytes())

    assert parsed.message_id == "<abc@example.com>"
    assert "Today was a good day." in parsed.plain_text
    assert len(parsed.attachments) == 1
    assert parsed.attachments[0].filename == "photo.jpg"
    assert parsed.attachments[0].content_type == "image/jpeg"
    assert parsed.attachments[0].data == b"jpeg-bytes"


def test_non_image_attachment_is_ignored():
    message = EmailMessage()
    message.set_content("entry")
    message.add_attachment(b"data", maintype="application", subtype="pdf", filename="file.pdf")

    assert parse_reply(message.as_bytes()).attachments == ()
