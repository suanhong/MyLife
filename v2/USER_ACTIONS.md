# User action gates

Development can continue without touching production until an external account or cloud write is needed.

## Gate 1: email integration

To test the defining reply-by-email workflow end to end, choose and authorize an email transport. Recommended default for this single-user service: Gmail API, using the user's Gmail account for outbound mail and polling replies by label/thread. Alternative: a transactional provider with inbound webhook support.

No email credential is needed in source control.

## Gate 2: staging cloud resources

Before migration writes, approve creation of a separate Cloud Run staging service and v2-only Datastore kinds / private Storage prefix or bucket. The legacy App Engine service remains untouched.

## Gate 3: recovered backup availability

The verified `mylife-backup.zip` must be made available to the staging migration command. Do not commit the backup to GitHub.
