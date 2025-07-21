import datetime
from uuid import UUID

from pydantic import BaseModel

from src.integration.domain.entities import Video


class Report(BaseModel):
    class ServiceReport(BaseModel):
        view_count: int
        video_count: int
        average_views: int
        top_video: Video | None = None

    # id: UUID
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime

    youtube: ServiceReport
    tiktok: ServiceReport
    instagram: ServiceReport