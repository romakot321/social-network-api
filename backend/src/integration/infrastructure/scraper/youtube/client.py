from src.core.config import settings
from src.core.http.client import IHttpClient
from src.integration.infrastructure.http_api_client import HttpApiClient
from src.integration.infrastructure.scraper.youtube.entities import YoutubeChannel, YoutubePlaylistItem, YoutubeVideo
from src.integration.infrastructure.scraper.youtube.schemas import YoutubeChannelsListResponse, \
    YoutubePlaylistItemsListResponse, YoutubeVideosListResponse


class YoutubeClient(HttpApiClient):
    api_key: str = settings.YOUTUBE_API_KEY

    def __init__(self, client: IHttpClient):
        super().__init__(client, source_url="https://www.googleapis.com")

    async def search_account(self, username: str) -> YoutubeChannel:
        response = await self.request("GET", "/youtube/v3/channels",
                                      params={"part": "contentDetails", "forHandle": username, "key": self.api_key})
        channels_response = self.validate_response(response.data, YoutubeChannelsListResponse)
        return channels_response.items[0]

    async def get_playlist_items(self, playlist_id: str) -> list[YoutubePlaylistItem]:
        response = await self.request("GET", "/youtube/v3/playlistItems",
                                      params={"part": 'contentDetails', 'playlistId': playlist_id, "key": self.api_key})
        items_response = self.validate_response(response.data, YoutubePlaylistItemsListResponse)
        return items_response.items

    async def get_videos(self, video_ids: list[str]) -> list[YoutubeVideo]:
        response = await self.request("GET", "/youtube/v3/videos",
                                      params={"part": "snippet,statistics", "id": ",".join(video_ids),
                                              "key": self.api_key})
        videos_response = self.validate_response(response.data, YoutubeVideosListResponse)
        return videos_response.items
