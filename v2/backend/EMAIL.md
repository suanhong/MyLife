# Email flow

The backend keeps mail provider details outside diary domain logic. Recommended first live adapter: Gmail API.

Daily flow: Cloud Scheduler calls an authenticated staging route in Asia/Seoul; v2 selects the nearest same-day anniversary entry; an opaque token is included in the subject; Gmail sends; only after a provider message ID is returned is that diary date marked sent. This fixes the legacy pre-send slug persistence failure mode.

Reply flow: scheduled Gmail polling finds MyLife replies; the token routes the message to the intended diary date; standard MIME parsing extracts text and images; Message-ID deduplication prevents repeated polling from duplicating entries; image MIME/size/signature is validated before private storage.

Live implementation requires Google account OAuth authorization. Credentials/tokens must never be committed to GitHub.
