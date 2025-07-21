import abc

from src.task.domain.entities import TaskItemCreate, TaskItem


class ITaskItemRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, data: TaskItemCreate) -> TaskItem: ...