from .mail_domain import token_from_subject
from .mail_parser import parse_reply


def route_reply(raw: bytes, token_store):
    parsed = parse_reply(raw)
    token = token_from_subject(parsed.subject)
    return parsed, (token_store.resolve(token) if token else None)
