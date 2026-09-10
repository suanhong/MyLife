def user_allowed(verified_email: str | None, owner_email: str | None) -> bool:
    if not verified_email or not owner_email:
        return False
    return verified_email.casefold() == owner_email.casefold()
