# Security

MyLife contains private diary text and photos. Cloud Storage objects must remain private; user-facing and scheduler routes require verified identity before production; OAuth/provider credentials belong in managed secrets, never Git; inbound attachments are MIME/size/signature validated; legacy Settings secrets are not part of portable migration; CI has no production deployment credentials; migration writes require an explicit flag and a separate v2 staging namespace.
