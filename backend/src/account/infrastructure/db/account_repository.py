from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, MissingGreenlet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.account.application.interfaces.account_repository import IAccountRepository
from src.account.domain.entities import AccountSearch, Account, AccountCreate
from src.account.infrastructure.db.orm import AccountDB
from src.db.exceptions import DBModelConflictException, DBModelNotFoundException


class PGAccountRepository(IAccountRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _flush(self):
        try:
            await self.session.flush()
        except IntegrityError as e:
            detail = "Model can't be created. " + str(e)
            raise DBModelConflictException(detail)

    async def create(self, data: AccountCreate) -> Account:
        model = AccountDB(**data.model_dump())
        self.session.add(model)
        await self._flush()
        return self._to_domain(model)

    async def get_list(self, params: AccountSearch) -> list[Account]:
        query = select(AccountDB).limit(params.count).offset(params.page * params.count)
        query = query.options(selectinload(AccountDB.profiles))
        if params.name:
            query = query.filter(AccountDB.name.like(f"%{params.name}%"))
        models = await self.session.scalars(query)
        return [self._to_domain(model) for model in models]

    async def get_by_pk(self, pk: UUID) -> Account:
        model = await self.session.get(AccountDB, pk, options=[selectinload(AccountDB.profiles)])
        if model is None:
            raise DBModelNotFoundException()
        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: AccountDB) -> Account:
        try:
            profiles = model.profiles
        except MissingGreenlet:
            profiles = []

        return Account(
            id=model.id,
            name=model.name,
            profiles=profiles,
        )