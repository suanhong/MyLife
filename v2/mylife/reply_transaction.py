"""Inbound reply transaction ordering.

Production implementation must not mark Message-ID processed before the diary
and attachments are durably stored. The in-memory helper in idempotency.py is
sufficient for unit tests but a Datastore transaction/claim state is required
for concurrent pollers. This module centralizes that invariant before provider
integration is enabled.
"""

PROCESSING = "processing"
PROCESSED = "processed"
