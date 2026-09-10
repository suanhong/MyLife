from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    project_id: str | None
    image_bucket: str | None
    timezone: str = "Asia/Seoul"
    owner_email: str | None = None
    scheduler_service_account: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
            image_bucket=os.getenv("MYLIFE_IMAGE_BUCKET"),
            timezone=os.getenv("MYLIFE_TIMEZONE", "Asia/Seoul"),
            owner_email=os.getenv("MYLIFE_OWNER_EMAIL"),
            scheduler_service_account=os.getenv("MYLIFE_SCHEDULER_SERVICE_ACCOUNT"),
        )
