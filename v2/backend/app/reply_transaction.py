"""Production reply-processing invariant.

A Message-ID must become PROCESSED only after diary text and image metadata/object
writes are durable. Concurrent Gmail pollers require a Datastore transaction or
lease/claim state. The current in-memory claim implementation is for tests only.
"""
PROCESSING = "processing"
PROCESSED = "processed"
