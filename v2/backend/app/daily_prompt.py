from datetime import date


def compose_daily_prompt(day: date, old_date: date | None = None, old_text: str | None = None):
    subject = f"MyLife diary - {day.isoformat()}"
    body = f"Write your diary for {day.isoformat()} by replying to this email."
    if old_date is not None and old_text is not None:
        body += f"\n\nOn this day: {old_date.isoformat()}\n\n{old_text}"
    return subject, body
