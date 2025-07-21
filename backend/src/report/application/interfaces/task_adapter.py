import abc
from uuid import UUID

from src.account.domain.entities import Service
from src.task.domain.dtos import TaskReadDTO, TaskListParamsDTO


class IReportTaskAdapter(abc.ABC):
    @abc.abstractmethod
    async def get_list(self, params: TaskListParamsDTO) -> list[TaskReadDTO]: ...

    @abc.abstractmethod
    async def get_account_last(self, account_id: UUID, service: Service) -> TaskReadDTO: ...