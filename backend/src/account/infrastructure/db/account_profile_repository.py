from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.application.interfaces.account_profile_repository import IAccountProfileRepository
from src.account.domain.entities import AccountProfile, AccountProfileCreate
from src.account.infrastructure.db.orm import AccountProfileDB
from src.db.exceptions import DBModelConflictException


class PGAccountProfileRepository(IAccountProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _flush(self):
        try:
            await self.session.flush()
        except IntegrityError as e:
            detail = "Model can't be created. " + str(e)
            raise DBModelConflictException(detail)

    async def create(self, data: AccountProfileCreate) -> AccountProfile:
        model = AccountProfileDB(**data.model_dump())
        self.session.add(model)
        await self._flush()
        return self._to_domain(model)

    async def get_list_for_account(self, account_id: UUID) -> list[AccountProfile]:
        query = select(AccountProfileDB).filter_by(account_id=account_id)
        models = await self.session.scalars(query)
        return [self._to_domain(model) for model in models]

    @staticmethod
    def _to_domain(model: AccountProfileDB) -> AccountProfile:
        return AccountProfile.model_validate(model)