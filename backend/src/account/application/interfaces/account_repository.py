import abc
from uuid import UUID

from src.account.domain.entities import AccountCreate, Account, AccountSearch


class IAccountRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, data: AccountCreate) -> Account: ...

    @abc.abstractmethod
    async def get_list(self, params: AccountSearch) -> list[Account]: ...

    @abc.abstractmethod
    async def get_by_pk(self, pk: UUID) -> Account: ...
