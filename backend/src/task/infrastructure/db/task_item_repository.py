from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.exceptions import DBModelConflictException
from src.task.application.interfaces.task_item_repository import ITaskItemRepository
from src.task.domain.entities import TaskItemCreate, TaskItem, TaskItemList
from src.task.infrastructure.db.orm import TaskItemDB, TaskDB


class PGTaskItemRepository(ITaskItemRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _flush(self):
        try:
            await self.session.flush()
        except IntegrityError as e:
            detail = "Model can't be created. " + str(e)
            raise DBModelConflictException(detail)

    async def create(self, data: TaskItemCreate) -> TaskItem:
        model = TaskItemDB(**data.model_dump())
        self.session.add(model)
        await self._flush()
        return self._to_domain(model)

    async def get_list(self, params: TaskItemList) -> list[TaskItem]:
        query = select(TaskItemDB).limit(params.count).offset(params.page * params.count).order_by(TaskItemDB.video_created_at)
        if params.tasks_ids:
            query = query.filter(TaskItemDB.task_id.in_(params.tasks_ids))
        if params.account_id:
            query = query.filter(TaskItemDB.task.has(TaskDB.account_id == params.account_id))

        models = await self.session.scalars(query)
        return [self._to_domain(model) for model in models]

    @staticmethod
    def _to_domain(model: TaskItemDB) -> TaskItem:
        return TaskItem.model_validate(model)