import secrets


def new_reply_token() -> str:
    return secrets.token_urlsafe(24)
