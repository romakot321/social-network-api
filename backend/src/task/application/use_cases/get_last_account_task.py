from http.client import HTTPException
from uuid import UUID

from src.account.domain.entities import Service
from src.db.exceptions import DBModelNotFoundException
from src.task.application.interfaces.task_account_adapter import ITaskAccountAdapter
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.domain.dtos import TaskReadDTO


class GetLastAccountTaskUseCase:
    def __init__(self, uow: ITaskUnitOfWork):
        self.uow = uow

    async def execute(self, account_id: UUID, service: Service) -> TaskReadDTO:
        async with self.uow:
            try:
                task = await self.uow.tasks.get_last_for_account(account_id, service)
            except DBModelNotFoundException:
                raise HTTPException(404)

        return TaskReadDTO(**task.model_dump())