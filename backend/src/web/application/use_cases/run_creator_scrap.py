import asyncio

from src.account.domain.dtos import AccountReadDTO
from src.account.domain.entities import Service
from src.core.http.client import IHttpClient
from src.task.application.interfaces.task_account_adapter import ITaskAccountAdapter
from src.task.application.interfaces.task_runner import ITaskRunner
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.application.use_cases.create_task import CreateTaskUseCase
from src.task.application.use_cases.run_task import RunTaskUseCase
from src.task.domain.dtos import TaskCreateDTO


class RunCreatorScrapUseCase:
    def __init__(self, task_uow: ITaskUnitOfWork, task_runner: ITaskRunner, account_adapter: ITaskAccountAdapter, http_client: IHttpClient):
        self.task_uow = task_uow
        self.task_runner = task_runner
        self.account_adapter = account_adapter
        self.http_client = http_client

    async def execute(self, account: AccountReadDTO):
        for service in Service:
            await self._run(account, service)

    async def _run(self, account: AccountReadDTO, service: Service):
        try:
            [profile for profile in account.profiles if profile.service == service][0]
        except IndexError:
            return

        data = TaskCreateDTO(account_id=account.id, service=service)
        task = await CreateTaskUseCase(self.task_uow).execute(data)
        asyncio.create_task(RunTaskUseCase(self.task_uow, self.task_runner, self.account_adapter, self.http_client).execute(task.id, data))
