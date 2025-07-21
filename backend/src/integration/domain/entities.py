import datetime

from pydantic import BaseModel


class Video(BaseModel):
    url: str
    title: str | None = None
    description: str | None = None
    thumbnail_url: str
    view_count: int
    created_at: datetime.datetime | None = None
