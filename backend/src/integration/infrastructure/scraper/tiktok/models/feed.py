from typing import ClassVar, List

from pydantic import BaseModel, HttpUrl, RootModel, Field


class AuthorInfo(BaseModel):
    id: str
    username: str | None = None
    nickname: str
    avatar: HttpUrl = Field(alias="avatarLarger")
    signature: str
    verified: bool

    class Config:
        fields: ClassVar[dict] = {
            "username": "uniqueId",
            "avatar": "avatarLarger",
            "is_verified": "verified",
        }


class AuthorStatsInfo(BaseModel):
    likes: int = Field(alias="diggCount")
    followers: int = Field(alias='followerCount')
    followings: int = Field(alias="followingCount")
    friends: int = Field(alias="friendCount")
    hearts: int = Field(alias="heartCount")
    videos: int = Field(alias="videoCount")


class MusicInfo(BaseModel):
    id: str
    title: str
    link: str = ""
    author_name: str = ""
    original: bool
    cover: str = ""

    class Config:
        fields: ClassVar[dict] = {
            "is_original": "original",
            "author_name": "authorName",
            "link": "playUrl",
            "cover": "coverLarge",
        }


class StatisticsInfo(BaseModel):
    plays: int = Field(alias="playCount")
    likes: int = Field(alias="diggCount")
    comments: int = Field(alias="commentCount")
    shares: int = Field(alias="shareCount")

    class Config:
        fields: ClassVar[dict] = {
            "likes": "diggCount",
            "shares": "shareCount",
            "comments": "commentCount",
            "plays": "playCount",
        }


class ChallengeInfo(BaseModel):
    id: str
    title: str
    desc: str
    profile_thumb: str = Field(alias="profileThumb")
    profile_medium: str = Field(alias="profileMedium")
    profile_larger: str = Field(alias="profileLarger")
    cover_thumb: str = Field("", alias="coverThumb")
    cover_medium: str = Field("", alias="coverMedium")
    cover_larger: str = Field("", alias="coverLarge")

    class Config:
        fields: ClassVar[dict] = {
            "profile_thumb": "profileThumb",
            "profile_medium": "profileMedium",
            "profile_larger": "profileLarger",
            "cover_thumb": "coverThumb",
            "cover_medium": "coverMedium",
            "cover_larger": "coverLarger",
        }


class VideoInfo(BaseModel):
    id: str
    height: int
    width: int
    duration: int
    ratio: str
    cover: HttpUrl
    play_addr: HttpUrl = Field(alias="playAddr")
    download_addr: HttpUrl = Field(alias="downloadAddr")

    class Config:
        fields: ClassVar[dict] = {
            "play_addr": "playAddr",
            "download_addr": "downloadAddr",
        }

    @property
    def original_video_url(self) -> str:
        return f"https://api2.musical.ly/aweme/v1/playwm/?video_id={self.id}"


class FeedItem(BaseModel):
    id: str
    desc: str
    create_time: int = Field(alias="createTime")
    author: AuthorInfo
    music: MusicInfo
    stats: StatisticsInfo
    author_stats: AuthorStatsInfo = Field(alias="authorStatsV2")
    video: VideoInfo
    challenges: List[ChallengeInfo] = []

    class Config:
        fields: ClassVar[dict] = {
            "create_time": "createTime",
        }


class FeedItems(RootModel):
    root: List[FeedItem]
