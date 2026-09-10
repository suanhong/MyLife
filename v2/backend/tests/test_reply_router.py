from datetime import date
from email.message import EmailMessage

from app.reply_router import route_reply


class Tokens:
    def resolve(self, token): return date(2026, 9, 10) if token == "abc" else None


def test_reply_routes_to_date():
    message = EmailMessage()
    message["Subject"] = "Re: Diary [MyLife:abc]"
    message.set_content("entry")
    _, day = route_reply(message.as_bytes(), Tokens())
    assert day == date(2026, 9, 10)
