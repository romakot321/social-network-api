import datetime

from src.account.domain.entities import Service
from src.core.http.client import AsyncHttpClient
from src.integration.domain.dtos import IntegrationTaskDTO, IntegrationTaskResultDTO, IntegrationTaskStatus
from src.integration.domain.entities import Video
from src.integration.infrastructure.scraper.tiktok.bot import TikTokPy
from src.integration.infrastructure.scraper.youtube.client import YoutubeClient
from src.task.application.interfaces.task_runner import ITaskRunner
from src.task.domain.entities import TaskRun


class TaskRunner(ITaskRunner[IntegrationTaskDTO]):
    async def start(self, data: TaskRun) -> IntegrationTaskDTO:
        if data.service == Service.tiktok:
            result = await self.start_tiktok(data.username)
        elif data.service == Service.youtube:
            result = await self.start_youtube(data.username)
        else:
            raise NotImplementedError(f"Service {data.service.name} not implemented")
        return IntegrationTaskDTO(status=IntegrationTaskStatus.finished, result=result, error=None)

    async def start_tiktok(self, username: str) -> IntegrationTaskResultDTO:
        async with TikTokPy() as bot:
            user_feed_items = await bot.user_feed(username=username, amount=1)  # Getting total videos count
            user_feed_items = await bot.user_feed(username=username, amount=user_feed_items[0].author_stats.videos)
        return IntegrationTaskResultDTO(
            service=Service.tiktok,
            username=username,
            videos=[
                Video(url=str(i.video.play_addr), thumbnail_url=str(i.video.cover), view_count=i.stats.plays, description=i.desc, created_at=datetime.datetime.fromtimestamp(i.created_time))
                for i in user_feed_items
            ]
        )

    async def start_youtube(self, username: str) -> IntegrationTaskResultDTO:
        client = YoutubeClient(AsyncHttpClient())
        channel = await client.search_account(username)
        upload_playlist_items = await client.get_playlist_items(channel.content_details.related_playlists.uploads)
        video_ids = [i.content_details.video_id for i in upload_playlist_items]
        videos = await client.get_videos(video_ids)
        return IntegrationTaskResultDTO(
            service=Service.youtube,
            username=username,
            videos=[Video(url=v.url, thumbnail_url=v.snippet.thumbnails.default.url, view_count=v.statistics.view_count, title=v.snippet.title, description=v.snippet.description, created_at=v.snippet.published_at) for v in videos]
        )
