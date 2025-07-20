from pydantic import BaseModel

from src.integration.infrastructure.scraper.youtube.entities import YoutubeChannel, YoutubePlaylistItem, YoutubeVideo


class YoutubeChannelsListResponse(BaseModel):
    items: list[YoutubeChannel]


class YoutubePlaylistItemsListResponse(BaseModel):
    items: list[YoutubePlaylistItem]


class YoutubeVideosListResponse(BaseModel):
    items: list[YoutubeVideo]
