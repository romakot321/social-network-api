from uuid import UUID

from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.domain.dtos import AccountProfileCreateDTO
from src.account.domain.entities import AccountProfileCreate, AccountProfile


class AddAccountProfileUseCase:
    def __init__(self, uow: IAccountUnitOfWork):
        self.uow = uow

    async def execute(self, account_id: UUID, dto: AccountProfileCreateDTO) -> AccountProfile:
        command = AccountProfileCreate(**dto.model_dump(), account_id=account_id)
        async with self.uow:
            profile = await self.uow.profiles.create(command)
            await self.uow.commit()
        return profile
