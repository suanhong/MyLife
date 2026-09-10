from dataclasses import dataclass


@dataclass(frozen=True)
class MailConfig:
    provider: str
    recipient: str

    def validate(self):
        if self.provider not in {"gmail", "smtp"}:
            raise ValueError("unsupported mail provider")
        if "@" not in self.recipient:
            raise ValueError("invalid recipient")
