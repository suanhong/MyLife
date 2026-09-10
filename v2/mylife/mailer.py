from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OutboundMessage:
    to: str
    subject: str
    text: str
    reply_token: str


@dataclass(frozen=True)
class SendReceipt:
    provider_message_id: str


class Mailer(Protocol):
    def send(self, message: OutboundMessage) -> SendReceipt: ...


def send_then_mark(message: OutboundMessage, mailer: Mailer, mark_sent) -> SendReceipt:
    """Persist sent state only after the provider returns a receipt."""
    receipt = mailer.send(message)
    mark_sent(receipt)
    return receipt
