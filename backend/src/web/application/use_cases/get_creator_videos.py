from uuid import UUID

from src.account.domain.entities import Service
from src.db.exceptions import DBModelNotFoundException
from src.integration.domain.entities import Video
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.domain.dtos import TaskReadResultDTO


class GetCreatorVideosUseCase:
    def __init__(self, task_uow: ITaskUnitOfWork):
        self.task_uow = task_uow

    async def execute(self, account_id: UUID) -> list[Video]:
        async with self.task_uow:
            try:
                last_tiktok_task = await self.task_uow.tasks.get_last_for_account(account_id, Service.tiktok)
                tiktok_videos = [Video(**i.model_dump()) for i in last_tiktok_task.items]
            except DBModelNotFoundException:
                tiktok_videos = []

            try:
                last_youtube_task = await self.task_uow.tasks.get_last_for_account(account_id, Service.youtube)
                youtube_videos = [Video(**i.model_dump()) for i in last_youtube_task.items]
            except DBModelNotFoundException:
                youtube_videos = []

        return tiktok_videos + youtube_videos
