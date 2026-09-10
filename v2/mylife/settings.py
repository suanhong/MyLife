from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    project_id: str | None
    image_bucket: str | None
    timezone: str = "Asia/Seoul"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
            image_bucket=os.getenv("MYLIFE_IMAGE_BUCKET"),
            timezone=os.getenv("MYLIFE_TIMEZONE", "Asia/Seoul"),
        )
