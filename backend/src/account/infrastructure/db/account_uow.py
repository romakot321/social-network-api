from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.infrastructure.db.account_profile_repository import PGAccountProfileRepository
from src.account.infrastructure.db.account_repository import PGAccountRepository
from src.db.engine import async_session_maker


class PGAccountUnitOfWork(IAccountUnitOfWork):
    def __init__(self, session_factory=async_session_maker):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.accounts = PGAccountRepository(self.session)
        self.profiles = PGAccountProfileRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def _rollback(self):
        await self.session.rollback()