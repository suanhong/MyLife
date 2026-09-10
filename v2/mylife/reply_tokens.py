import secrets


def new_reply_token() -> str:
    """Opaque token suitable for mapping an inbound reply to one diary date."""
    return secrets.token_urlsafe(24)
