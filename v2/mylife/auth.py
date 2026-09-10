from __future__ import annotations


def user_allowed(verified_email: str | None, owner_email: str | None) -> bool:
    """Single-user authorization rule after platform identity verification."""
    if not verified_email or not owner_email:
        return False
    return verified_email.casefold() == owner_email.casefold()
