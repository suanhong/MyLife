from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DailyPrompt:
    diary_date: date
    reply_token: str
    old_post_date: date | None = None


def should_send_daily_prompt(*, already_sent: bool, local_date: date, requested_date: date) -> bool:
    """A prompt is eligible once for its intended local calendar date.

    Persistence of `already_sent=True` must happen only after the mail provider
    confirms acceptance. This prevents the legacy failure mode where a slug was
    persisted before send and then suppressed retries after a transient failure.
    """
    return local_date == requested_date and not already_sent
