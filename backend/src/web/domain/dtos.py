import datetime
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel


class CreatorReadDTO(BaseModel):
    name: str
    account_id: UUID
    youtube_total_views: str
    instagram_total_views: str
    tiktok_total_views: str
    total_views: str
    total_videos: int
    big_videos: int
    fotobudka_income: int


class CreatorCreateDTO(BaseModel):
    name: str
    youtube_username: str | None = None
    tiktok_username: str | None = None
    instagram_username: str | None = None
    fotobudka_url: str | None = None

    @classmethod
    def as_form(cls, name: str = Form(), youtube_username: str | None = Form(None), tiktok_username: str | None = Form(None), instagram_username: str | None = Form(None), fotobudka_url: str | None = Form(None)):
        return cls(name=name, youtube_username=youtube_username, tiktok_username=tiktok_username, instagram_username=instagram_username, fotobudka_url=fotobudka_url)


class CreatorVideosListParamsDTO(BaseModel):
    from_created_at: datetime.datetime | None = None
    to_created_at: datetime.datetime | None = None
    count: int = 25
    page: int = 0
