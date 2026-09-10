from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OutboundMail:
    recipient: str
    subject: str
    text: str


@dataclass(frozen=True)
class MailReceipt:
    provider_message_id: str


class Mailer(Protocol):
    def send(self, message: OutboundMail) -> MailReceipt: ...
