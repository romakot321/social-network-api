from uuid import UUID

from src.account.domain.entities import Service
from src.report.application.interfaces.task_adapter import IReportTaskAdapter
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.application.use_cases.get_last_account_task import GetLastAccountTaskUseCase
from src.task.application.use_cases.get_tasks_list import GetTasksListUseCase
from src.task.domain.dtos import TaskListParamsDTO, TaskReadDTO


class ReportTaskAdapter(IReportTaskAdapter):
    def __init__(self, uow: ITaskUnitOfWork):
        self.uow = uow

    async def get_list(self, params: TaskListParamsDTO) -> list[TaskReadDTO]:
        return await GetTasksListUseCase(self.uow).execute(params)

    async def get_account_last(self, account_id: UUID, service: Service) -> TaskReadDTO:
        return await GetLastAccountTaskUseCase(self.uow).execute(account_id, service)
