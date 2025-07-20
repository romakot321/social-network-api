from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.domain.dtos import AccountListParamsDTO, AccountReadDTO
from src.account.domain.entities import AccountSearch


class GetAccountsListUseCase:
    def __init__(self, uow: IAccountUnitOfWork):
        self.uow = uow

    async def execute(self, dto: AccountListParamsDTO) -> list[AccountReadDTO]:
        command = AccountSearch(**dto.model_dump(exclude_unset=True))
        async with self.uow:
            accounts = await self.uow.accounts.get_list(command)
        return [AccountReadDTO.model_validate(account) for account in accounts]
