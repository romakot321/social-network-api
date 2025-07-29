from uuid import UUID

from src.account.domain.entities import Service
from src.db.exceptions import DBModelNotFoundException
from src.integration.domain.entities import Video
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.domain.dtos import TaskReadResultDTO
from src.task.domain.entities import TaskItemList
from src.web.domain.dtos import CreatorVideosListParamsDTO


class GetCreatorVideosUseCase:
    def __init__(self, task_uow: ITaskUnitOfWork):
        self.task_uow = task_uow

    async def execute(self, account_id: UUID, dto: CreatorVideosListParamsDTO) -> list[Video]:
        async with self.task_uow:
            tasks_ids = []

            for service in Service:
                try:
                    last_task = await self.task_uow.tasks.get_last_for_account(account_id, service)
                    tasks_ids.append(last_task.id)
                except DBModelNotFoundException:
                    continue

            videos = await self.task_uow.items.get_list(TaskItemList(tasks_ids=tasks_ids, page=dto.page, count=dto.count))
            videos = [Video(**i.model_dump()) for i in videos]

        return videos
