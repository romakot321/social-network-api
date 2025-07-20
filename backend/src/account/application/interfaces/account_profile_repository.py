import abc
from uuid import UUID

from src.account.domain.entities import AccountProfileCreate, AccountProfile


class IAccountProfileRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, data: AccountProfileCreate) -> AccountProfile: ...

    @abc.abstractmethod
    async def get_list_for_account(self, account_id: UUID) -> list[AccountProfile]: ...
