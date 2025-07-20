from uuid import UUID

from fastapi import Form
from pydantic import BaseModel


class CreatorReadDTO(BaseModel):
    name: str
    account_id: UUID
    youtube_total_views: int
    instagram_total_views: int
    tiktok_total_views: int


class CreatorCreateDTO(BaseModel):
    name: str
    youtube_username: str | None = None
    tiktok_username: str | None = None
    instagram_username: str | None = None

    @classmethod
    def as_form(cls, name: str = Form(), youtube_username: str | None = Form(None), tiktok_username: str | None = Form(None), instagram_username: str | None = Form(None)):
        return cls(name=name, youtube_username=youtube_username, tiktok_username=tiktok_username, instagram_username=instagram_username)