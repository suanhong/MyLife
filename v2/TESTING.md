# Test strategy

CI runs Python 3.12 unit/integration tests and builds the Cloud Run container. Tests use in-memory adapters unless they specifically exercise serialization or adapter contracts, so CI cannot alter Google Cloud data.

Critical regression cases include: daily send state only after provider success; retry after transient send failure; reply Message-ID deduplication; reply-token routing; image MIME/signature/size validation; multi-part MIME parsing; anniversary selection; Asia/Seoul date resolution; portable backup CRC/hash checks; legacy count/reference mapping; migration writes disabled by default; diary CRUD/listing.

Live staging tests will be added only after email authorization and separate Cloud Run/storage configuration are approved.
