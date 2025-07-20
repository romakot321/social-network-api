from uuid import UUID

from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.domain.entities import Service
from src.db.exceptions import DBModelConflictException, DBModelNotFoundException
from src.task.application.interfaces.task_repository import ITaskRepository
from src.task.domain.entities import Task, TaskCreate, TaskStatus, TaskUpdate
from src.task.infrastructure.db.orm import TaskDB


class PGTaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _flush(self):
        try:
            await self.session.flush()
        except IntegrityError as e:
            detail = "Model can't be created. " + str(e)
            raise DBModelConflictException(detail)

    async def create(self, data: TaskCreate) -> Task:
        model = TaskDB(**(data.model_dump() | {"status": "queued"}))
        self.session.add(model)
        await self._flush()
        return self._to_domain(model)

    async def get_by_pk(self, pk: UUID) -> Task:
        model = await self.session.get(TaskDB, pk)
        if model is None:
            raise DBModelNotFoundException()
        return self._to_domain(model)

    async def update_by_pk(self, pk: UUID, data: TaskUpdate) -> Task:
        query = update(TaskDB).filter_by(id=pk).values(**data.model_dump(mode="json", exclude_none=True))
        result = await self.session.execute(query)
        if result.rowcount == 0:
            raise DBModelNotFoundException()
        await self._flush()
        return await self.get_by_pk(pk)

    async def get_last_for_account(self, account_id: UUID, service: Service) -> Task:
        query = select(TaskDB).filter_by(account_id=account_id, service=service.value).order_by(TaskDB.created_at.desc()).limit(1)
        query = query.filter_by(status="finished")
        model = await self.session.scalar(query)
        if model is None:
            raise DBModelNotFoundException()
        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: TaskDB) -> Task:
        return Task(
            id=model.id,
            account_id=model.account_id,
            service=Service(model.service),
            status=TaskStatus(model.status),
            result=model.result,
            error=model.error
        )
