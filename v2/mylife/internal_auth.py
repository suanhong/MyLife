from __future__ import annotations


def scheduler_request_allowed(headers, expected_service_account: str | None) -> bool:
    """Authorization hook for internal scheduler routes.

    Cloud Run should enforce IAM before the request reaches Flask. This function
    additionally checks an identity value supplied by trusted middleware after
    token verification; raw user-supplied headers must not be trusted directly.
    """
    if not expected_service_account:
        return False
    return headers.get("X-Verified-Service-Account") == expected_service_account
