from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.domain.dtos import AccountCreateDTO, AccountReadDTO
from src.account.domain.entities import AccountCreate


class AddAccountUseCase:
    def __init__(self, uow: IAccountUnitOfWork):
        self.uow = uow

    async def execute(self, dto: AccountCreateDTO) -> AccountReadDTO:
        command = AccountCreate(**dto.model_dump())
        async with self.uow:
            account = await self.uow.accounts.create(command)
            await self.uow.commit()
        return AccountReadDTO(**account.model_dump())
