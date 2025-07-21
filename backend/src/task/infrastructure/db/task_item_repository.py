from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.exceptions import DBModelConflictException
from src.task.application.interfaces.task_item_repository import ITaskItemRepository
from src.task.domain.entities import TaskItemCreate, TaskItem
from src.task.infrastructure.db.orm import TaskItemDB


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

    @staticmethod
    def _to_domain(model: TaskItemDB) -> TaskItem:
        return TaskItem.model_validate(model)