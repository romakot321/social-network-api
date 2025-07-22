from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.domain.dtos import AccountListParamsDTO
from src.account.domain.entities import AccountSearch, Service, Account
from src.db.exceptions import DBModelNotFoundException
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.domain.dtos import TaskReadDTO, TaskResultDTO, TaskReadResultDTO
from src.web.domain.dtos import CreatorReadDTO


class GetCreatorsListUseCase:
    def __init__(self, task_uow: ITaskUnitOfWork, account_uow: IAccountUnitOfWork):
        self.task_uow = task_uow
        self.account_uow = account_uow

    async def execute(self, dto: AccountListParamsDTO) -> list[CreatorReadDTO]:
        params = AccountSearch(**dto.model_dump())
        async with self.account_uow:
            accounts = await self.account_uow.accounts.get_list(params)

        async with self.task_uow:
            creators = [
                CreatorReadDTO(
                    name=account.name,
                    account_id=account.id,
                    tiktok_total_views=await self._calculate_total_views(account, Service.tiktok),
                    youtube_total_views=await self._calculate_total_views(account, Service.youtube),
                    instagram_total_views=0
                )
                for account in accounts
            ]

        return creators

    async def _calculate_total_views(self, account: Account, service: Service) -> int:
        try:
            last_task = await self.task_uow.tasks.get_last_for_account(account.id, service)
        except DBModelNotFoundException:
            return 0

        return sum(i.view_count for i in last_task.items)
