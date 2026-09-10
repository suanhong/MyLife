from dataclasses import dataclass


@dataclass(frozen=True)
class EmailConfig:
    provider: str
    recipient: str

    def validate(self) -> None:
        if self.provider not in {"gmail", "smtp"}:
            raise ValueError("unsupported email provider")
        if "@" not in self.recipient:
            raise ValueError("invalid recipient")
