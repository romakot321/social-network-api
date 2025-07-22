import abc

from src.task.domain.entities import TaskItemCreate, TaskItem, TaskItemList


class ITaskItemRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, data: TaskItemCreate) -> TaskItem: ...

    @abc.abstractmethod
    async def get_list(self, params: TaskItemList) -> list[TaskItem]: ...