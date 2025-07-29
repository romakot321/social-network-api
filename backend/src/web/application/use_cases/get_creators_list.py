import datetime
from uuid import uuid4

import humanize

from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.domain.dtos import AccountListParamsDTO
from src.account.domain.entities import AccountSearch, Service, Account
from src.db.exceptions import DBModelNotFoundException
from src.integration.infrastructure.fotobudka.client import FotobudkaClient
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.domain.dtos import TaskReadDTO, TaskResultDTO, TaskReadResultDTO
from src.web.domain.dtos import CreatorReadDTO

humanize.i18n.activate("ru_RU")


class GetCreatorsListUseCase:
    def __init__(self, task_uow: ITaskUnitOfWork, account_uow: IAccountUnitOfWork, fotobudka_client: FotobudkaClient):
        self.task_uow = task_uow
        self.account_uow = account_uow
        self.fotobudka_client = fotobudka_client

    async def execute(self, dto: AccountListParamsDTO) -> list[CreatorReadDTO]:
        params = AccountSearch(**dto.model_dump())
        async with self.account_uow:
            accounts = await self.account_uow.accounts.get_list(params)

        creators = []
        total = CreatorReadDTO(
            name="Итого",
            account_id=uuid4(),
            youtube_total_views='0',
            tiktok_total_views='0',
            instagram_total_views='0',
            total_views='0',
            total_videos=0,
            big_videos=0,
            fotobudka_income=0
        )

        async with self.task_uow:
            for account in accounts:
                tiktok_views, tiktok_videos, tiktok_big_videos = await self._calculate_total_views_videos(account, Service.tiktok, dto.stats_from, dto.stats_to)
                youtube_views, youtube_videos, youtube_big_videos = await self._calculate_total_views_videos(account, Service.youtube, dto.stats_from, dto.stats_to)
                instagram_views, instagram_videos, instagram_big_videos = await self._calculate_total_views_videos(account, Service.instagram, dto.stats_from, dto.stats_to)
                fotobudka_income = await self._get_fotobudka_income(account)

                creator = CreatorReadDTO(
                    name=account.name,
                    account_id=account.id,
                    tiktok_total_views=humanize.intword(tiktok_views),
                    youtube_total_views=humanize.intword(youtube_views),
                    instagram_total_views=humanize.intword(instagram_views),
                    total_views=humanize.intword(tiktok_views + youtube_views + instagram_views),
                    total_videos=tiktok_videos + youtube_videos + instagram_videos,
                    big_videos=tiktok_big_videos + youtube_big_videos + instagram_big_videos,
                    fotobudka_income=fotobudka_income
                )
                total.tiktok_total_views = str(int(total.tiktok_total_views) + int(tiktok_views))
                total.youtube_total_views = str(int(total.youtube_total_views) + int(youtube_views))
                total.instagram_total_views = str(int(total.instagram_total_views) + int(instagram_views))
                total.total_views = str(int(total.total_views) + tiktok_views + youtube_views + instagram_views)
                total.total_videos = int(total.total_videos) + int(creator.total_videos)
                total.big_videos = int(total.big_videos) + int(creator.big_videos)
                creators.append(creator)

        total = CreatorReadDTO(
            name="Итого",
            account_id=uuid4(),
            youtube_total_views=humanize.intword(total.youtube_total_views),
            tiktok_total_views=humanize.intword(total.tiktok_total_views),
            instagram_total_views=humanize.intword(total.instagram_total_views),
            total_views=humanize.intword(total.total_views),
            total_videos=total.total_videos,
            big_videos=total.big_videos,
            fotobudka_income=sum([c.fotobudka_income for c in creators])
        )

        creators.append(total)

        return creators

    async def _get_fotobudka_income(self, account: Account) -> int:
        profile = [p for p in account.profiles if p.service is Service.fotobudka]
        if not profile:
            return 0
        response = await self.fotobudka_client.get_partner_stat(profile[0].service_username)
        return response.data.amount

    async def _calculate_total_views_videos(self, account: Account, service: Service, from_datetime: datetime.datetime | None, to_datetime: datetime.datetime | None) -> tuple[int, int, int]:
        try:
            last_task = await self.task_uow.tasks.get_last_for_account(account.id, service)
        except DBModelNotFoundException:
            return 0, 0, 0

        items = last_task.items
        if from_datetime:
            items = filter(lambda i: i.video_created_at >= from_datetime, items)
        if to_datetime:
            items = filter(lambda i: i.video_created_at <= to_datetime, items)
        items = list(items)

        return (
            sum(i.view_count for i in items),
            len(items),
            len([i for i in items if i.view_count >= 1000000])
        )
