from uuid import UUID

from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.domain.dtos import AccountProfileReadDTO


class GetAccountProfilesListUseCase:
    def __init__(self, uow: IAccountUnitOfWork):
        self.uow = uow

    async def execute(self, account_id: UUID) -> list[AccountProfileReadDTO]:
        async with self.uow:
            profiles = await self.uow.profiles.get_list_for_account(account_id)
        return [AccountProfileReadDTO.model_validate(profile) for profile in profiles]
