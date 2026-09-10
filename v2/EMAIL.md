# Email integration

The v2 domain is provider-neutral. The proposed first implementation is Gmail API because MyLife is a single-user service and the user already interacts with the diary through normal email replies.

## Proposed flow

1. Cloud Scheduler invokes the authenticated daily job in Asia/Seoul.
2. v2 composes the prompt and optional anniversary entry.
3. Gmail API sends the prompt.
4. Only after Gmail returns a message ID does v2 mark that date sent.
5. A separate scheduled poll reads replies matching the MyLife label/thread.
6. Standard-library MIME parsing extracts the new body and image attachments.
7. Message-ID deduplication makes repeated polls safe.
8. Validated images go to private Cloud Storage and the diary stores stable image IDs.

The implementation requires OAuth/Google account authorization, so live Gmail testing is a user-action gate. No Gmail token should be committed to GitHub.
