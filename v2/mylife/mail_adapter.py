from __future__ import annotations

from typing import Protocol

from .mailer import Mailer


class ReplySource(Protocol):
    def fetch_unprocessed(self) -> list[bytes]: ...
    def mark_processed(self, provider_id: str) -> None: ...


class EmailIntegration(Protocol):
    mailer: Mailer
    replies: ReplySource
