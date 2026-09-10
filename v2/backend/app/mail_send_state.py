from __future__ import annotations


def send_then_mark(message, mailer, mark_sent):
    """Never suppress a retry because state was persisted before provider success."""
    receipt = mailer.send(message)
    mark_sent(receipt)
    return receipt
