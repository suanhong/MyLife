# Legacy migration contract

The verified recovery snapshot used for migration contains 2,822 diary Posts, 252 UserImage entities/original photo files, 252 unique image references across 251 diary posts, and no missing local original images. The independently downloaded ZIP passed CRC validation and its SHA-256 was verified after transfer to the user's PC.

The v2 importer must reject count/reference mismatches before any writes. Import into a staging namespace/service first. Legacy Datastore kinds and legacy GCS object names are read-only migration inputs and are never mutated by the v2 importer.

The production migration implementation still needs an explicit mapping from legacy `Post.images` key strings to `UserImage` metadata and then to v2 image IDs. That mapping will be tested against the portable backup before any cloud write is enabled.
