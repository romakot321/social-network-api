import asyncio
from uuid import UUID

from loguru import logger

from src.core.http.client import IHttpClient
from src.integration.domain.exceptions import IntegrationRequestException
from src.task.application.interfaces.task_account_adapter import ITaskAccountAdapter
from src.task.application.interfaces.task_runner import ITaskRunner
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.domain.dtos import TaskReadDTO, TaskCreateDTO, TaskResultDTO
from src.task.domain.entities import Task, TaskRun, TaskStatus, TaskUpdate, TaskItemCreate
from src.task.domain.mappers import IntegrationResponseToDomainMapper


class RunTaskUseCase:
    TIMEOUT_SECONDS = 30 * 60

    def __init__(
            self,
            uow: ITaskUnitOfWork,
            runner: ITaskRunner,
            account_adapter: ITaskAccountAdapter,
            http_client: IHttpClient,
    ) -> None:
        self.uow = uow
        self.runner = runner
        self.http_client = http_client
        self.account_adapter = account_adapter

    async def execute(self, task_id: UUID, dto: TaskCreateDTO) -> None:
        """Run it in background"""
        service_username = await self.account_adapter.get_account_profile_username(dto.account_id, dto.service)

        command = TaskRun(**dto.model_dump(), username=service_username)
        logger.info(f"Running task {task_id}")
        logger.debug(f"Task {task_id} params: {command}")
        task, error = await self._run(command)

        if error is not None or task is None:
            task = await self._store_error(task_id, status=TaskStatus.failed, error=error)
            await self._send_webhook(task_id, TaskResultDTO(**task.model_dump()), dto.webhook_url)
            return

        logger.info(f"Task {task_id} result: {task.model_dump_json(exclude='result')}")
        task = await self._store_result(task_id, task)
        await self._send_webhook(task_id, TaskResultDTO(**task.model_dump()), dto.webhook_url)

    async def _send_webhook(self, task_id: UUID, result: TaskResultDTO, webhook_url: str | None):
        if webhook_url is None:
            return
        data = TaskReadDTO(id=task_id, **result.model_dump())
        response = await self.http_client.post(str(webhook_url), json=data.model_dump(mode="json"))
        logger.debug(f"Sended webhook {task_id=}: {response}")

    async def _store_result(self, task_id: UUID, result: TaskResultDTO) -> Task:
        async with self.uow:
            task = await self.uow.tasks.update_by_pk(
                task_id, TaskUpdate(status=result.status, error=result.error)
            )
            for item in result.items:
                await self.uow.items.create(TaskItemCreate(task_id=task_id, **item.model_dump()))
            await self.uow.commit()
        return task

    async def _store_error(self, task_id: UUID, status: TaskStatus, error: str | None = None) -> Task:
        async with self.uow:
            task = await self.uow.tasks.update_by_pk(task_id, TaskUpdate(status=status, error=error))
            await self.uow.commit()
        return task

    async def _run(self, command: TaskRun) -> tuple[TaskResultDTO | None, None | str]:
        try:
            result = await asyncio.wait_for(self.runner.start(command), timeout=self.TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            return None, "Generation run error: Timeout"
        except IntegrationRequestException as e:
            logger.opt(exception=True).warning(e)
            return None, "Request error: " + str(e)
        except Exception as e:
            logger.exception(e)
            return None, "Internal exception"

        result_domain = IntegrationResponseToDomainMapper().map_one(result)
        return result_domain, None
