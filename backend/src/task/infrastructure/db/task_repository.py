from uuid import UUID

from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError, MissingGreenlet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.account.domain.entities import Service
from src.db.exceptions import DBModelConflictException, DBModelNotFoundException
from src.task.application.interfaces.task_repository import ITaskRepository
from src.task.domain.entities import Task, TaskCreate, TaskStatus, TaskUpdate, TaskList
from src.task.infrastructure.db.orm import TaskDB, TaskItemDB


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
        model = await self.session.get(TaskDB, pk, options=[selectinload(TaskDB.items)])
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

    async def get_list(self, params: TaskList) -> list[Task]:
        query = select(TaskDB)
        if params.from_created_at:
            query = query.filter(TaskDB.created_at >= params.from_created_at)
        if params.to_created_at:
            query = query.filter(TaskDB.created_at <= params.to_created_at)
        if params.from_video_created_at:
            query = query.filter(TaskDB.items.any(TaskItemDB.video_created_at >= params.from_video_created_at))
        if params.to_video_created_at:
            query = query.filter(TaskDB.items.any(TaskItemDB.video_created_at <= params.to_video_created_at))
        if params.account_id:
            query = query.filter_by(account_id=params.account_id)
        if params.service:
            query = query.filter_by(service=params.service.value)
        query = query.order_by(TaskDB.created_at.desc())

        models = await self.session.scalars(query)
        return [self._to_domain(model) for model in models]

    @staticmethod
    def _to_domain(model: TaskDB) -> Task:
        try:
            items = model.items
        except MissingGreenlet:
            items = []

        return Task(
            id=model.id,
            account_id=model.account_id,
            service=Service(model.service),
            status=TaskStatus(model.status),
            items=items,
            error=model.error
        )
