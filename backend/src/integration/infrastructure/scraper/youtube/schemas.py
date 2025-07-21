from pydantic import BaseModel, Field

from src.integration.infrastructure.scraper.youtube.entities import YoutubeChannel, YoutubePlaylistItem, YoutubeVideo


class YoutubeChannelsListResponse(BaseModel):
    items: list[YoutubeChannel]


class YoutubePlaylistItemsListResponse(BaseModel):
    next_page_token: str | None = Field(None, alias="nextPageToken")
    items: list[YoutubePlaylistItem]


class YoutubeVideosListResponse(BaseModel):
    items: list[YoutubeVideo]
