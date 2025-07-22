from uuid import uuid4

import humanize

from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.domain.dtos import AccountListParamsDTO
from src.account.domain.entities import AccountSearch, Service, Account
from src.db.exceptions import DBModelNotFoundException
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.domain.dtos import TaskReadDTO, TaskResultDTO, TaskReadResultDTO
from src.web.domain.dtos import CreatorReadDTO

humanize.i18n.activate("ru_RU")


class GetCreatorsListUseCase:
    def __init__(self, task_uow: ITaskUnitOfWork, account_uow: IAccountUnitOfWork):
        self.task_uow = task_uow
        self.account_uow = account_uow

    async def execute(self, dto: AccountListParamsDTO) -> list[CreatorReadDTO]:
        params = AccountSearch(**dto.model_dump())
        async with self.account_uow:
            accounts = await self.account_uow.accounts.get_list(params)

        creators = []

        async with self.task_uow:
            for account in accounts:
                tiktok_views, tiktok_videos, tiktok_big_videos = await self._calculate_total_views_videos(account, Service.tiktok)
                youtube_views, youtube_videos, youtube_big_videos = await self._calculate_total_views_videos(account, Service.youtube)
                instagram_views, instagram_videos, instagram_big_videos = await self._calculate_total_views_videos(account, Service.instagram)

                creator = CreatorReadDTO(
                    name=account.name,
                    account_id=account.id,
                    tiktok_total_views=humanize.intword(tiktok_views),
                    youtube_total_views=humanize.intword(youtube_views),
                    instagram_total_views=humanize.intword(instagram_views),
                    total_views=humanize.intword(tiktok_views + youtube_views + instagram_views),
                    total_videos=tiktok_videos + youtube_videos + instagram_videos,
                    big_videos=tiktok_big_videos + youtube_big_videos + instagram_big_videos
                )
                creators.append(creator)

        creators.append(
            CreatorReadDTO(
                name="Итого",
                account_id=uuid4(),
                youtube_total_views=humanize.intword(sum([c.youtube_total_views for c in creators])),
                tiktok_total_views=humanize.intword(sum([c.tiktok_total_views for c in creators])),
                instagram_total_views=humanize.intword(sum([c.instagram_total_views for c in creators])),
                total_views=humanize.intword(sum([c.total_views for c in creators])),
                total_videos=sum([c.total_videos for c in creators]),
                big_videos=sum([c.big_videos for c in creators]),
            )
        )

        return creators

    async def _calculate_total_views_videos(self, account: Account, service: Service) -> tuple[int, int, int]:
        try:
            last_task = await self.task_uow.tasks.get_last_for_account(account.id, service)
        except DBModelNotFoundException:
            return 0, 0, 0

        return (
            sum(i.view_count for i in last_task.items),
            len(last_task.items),
            len([i for i in last_task.items if i.view_count >= 1000000])
        )
