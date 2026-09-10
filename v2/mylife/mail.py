from __future__ import annotations

from dataclasses import dataclass
from email import policy
from email.parser import BytesParser


@dataclass(frozen=True)
class Attachment:
    filename: str
    content_type: str
    content_id: str | None
    data: bytes


@dataclass(frozen=True)
class ParsedReply:
    message_id: str | None
    plain_text: str | None
    html_text: str | None
    attachments: tuple[Attachment, ...]


def parse_reply(raw_message: bytes) -> ParsedReply:
    message = BytesParser(policy=policy.default).parsebytes(raw_message)
    plain = None
    html = None
    attachments = []

    for part in message.walk():
        if part.is_multipart():
            continue
        content_type = part.get_content_type()
        disposition = part.get_content_disposition()
        filename = part.get_filename()

        if disposition == "attachment" or filename:
            if content_type.startswith("image/") and filename:
                attachments.append(Attachment(
                    filename=filename,
                    content_type=content_type,
                    content_id=(part.get("Content-ID") or "").strip("<>") or None,
                    data=part.get_payload(decode=True) or b"",
                ))
            continue

        if content_type == "text/plain" and plain is None:
            plain = part.get_content()
        elif content_type == "text/html" and html is None:
            html = part.get_content()

    return ParsedReply(
        message_id=message.get("Message-ID"),
        plain_text=plain,
        html_text=html,
        attachments=tuple(attachments),
    )
