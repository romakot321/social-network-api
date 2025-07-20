import abc

from src.account.application.interfaces.account_profile_repository import IAccountProfileRepository
from src.account.application.interfaces.account_repository import IAccountRepository


class IAccountUnitOfWork(abc.ABC):
    accounts: IAccountRepository
    profiles: IAccountProfileRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._rollback()

    @abc.abstractmethod
    async def commit(self): ...

    @abc.abstractmethod
    async def _rollback(self): ...
