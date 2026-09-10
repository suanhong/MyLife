from __future__ import annotations

from dataclasses import dataclass
from email import policy
from email.parser import BytesParser


@dataclass(frozen=True)
class MailAttachment:
    filename: str
    content_type: str
    content_id: str | None
    data: bytes


@dataclass(frozen=True)
class ParsedMail:
    message_id: str | None
    subject: str
    plain_text: str | None
    html_text: str | None
    attachments: tuple[MailAttachment, ...]


def parse_reply(raw: bytes) -> ParsedMail:
    message = BytesParser(policy=policy.default).parsebytes(raw)
    plain = html = None
    attachments = []
    for part in message.walk():
        if part.is_multipart():
            continue
        content_type = part.get_content_type()
        filename = part.get_filename()
        if filename:
            if content_type.startswith("image/"):
                attachments.append(MailAttachment(filename, content_type,
                    (part.get("Content-ID") or "").strip("<>") or None,
                    part.get_payload(decode=True) or b""))
            continue
        if content_type == "text/plain" and plain is None:
            plain = part.get_content()
        elif content_type == "text/html" and html is None:
            html = part.get_content()
    return ParsedMail(message.get("Message-ID"), message.get("Subject", ""), plain, html, tuple(attachments))
