def scheduler_allowed(verified_service_account: str | None, expected: str | None) -> bool:
    return bool(verified_service_account and expected and verified_service_account == expected)
