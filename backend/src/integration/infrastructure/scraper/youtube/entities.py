import datetime

from pydantic import BaseModel, Field


class YoutubeChannel(BaseModel):
    class ContentDetails(BaseModel):
        class RelatedPlaylists(BaseModel):
            likes: str
            uploads: str

        related_playlists: RelatedPlaylists = Field(alias="relatedPlaylists")

    id: str
    content_details: ContentDetails = Field(alias="contentDetails")


class YoutubePlaylistItem(BaseModel):
    class ContentDetails(BaseModel):
        video_id: str = Field(alias="videoId")
        video_published_at: datetime.datetime = Field(alias="videoPublishedAt")

    id: str
    content_details: ContentDetails = Field(alias="contentDetails")


class YoutubeVideo(BaseModel):
    class Snippet(BaseModel):
        class Thumbnails(BaseModel):
            class Thumbnail(BaseModel):
                url: str

            default: Thumbnail

        title: str
        description: str
        thumbnails: Thumbnails

    class Statistics(BaseModel):
        view_count: int = Field(alias="viewCount")

    id: str
    snippet: Snippet
    statistics: Statistics

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.id}"
