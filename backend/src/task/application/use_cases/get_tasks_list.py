from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.domain.dtos import TaskListParamsDTO, TaskReadDTO
from src.task.domain.entities import TaskList


class GetTasksListUseCase:
    def __init__(self, uow: ITaskUnitOfWork):
        self.uow = uow

    async def execute(self, dto: TaskListParamsDTO) -> list[TaskReadDTO]:
        command = TaskList(**dto.model_dump())
        async with self.uow:
            tasks = await self.uow.tasks.get_list(command)
        return [TaskReadDTO.model_validate(task) for task in tasks]