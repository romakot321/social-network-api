from uuid import UUID

from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.domain.dtos import AccountReadDTO


class GetAccountUseCase:
    def __init__(self, uow: IAccountUnitOfWork):
        self.uow = uow

    async def execute(self, account_id: UUID) -> AccountReadDTO:
        async with self.uow:
            account = await self.uow.accounts.get_by_pk(account_id)
        return AccountReadDTO.model_validate(account)