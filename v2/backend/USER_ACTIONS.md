# Next user-action gates

Code-only foundation work can proceed without touching production. The first unavoidable external gates are:

1. Email: choose/authorize the account/provider used for outbound diary prompts and inbound replies. Gmail API is the recommended default for this single-user workflow; no token belongs in GitHub.
2. Staging: approve creation/deployment of a separate Cloud Run staging service and v2-only Datastore namespace/private Storage location. The legacy App Engine service remains untouched.
3. Migration: make the already verified `mylife-backup.zip` available to the staging import command. The ZIP must not be committed to GitHub.

Until these gates are approved, CI remains test/build only and migration commands default to read-only/dry-run behavior.
