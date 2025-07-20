import json

from src.integration.domain.dtos import IntegrationTaskDTO, IntegrationTaskStatus
from src.task.domain.dtos import TaskResultDTO
from src.task.domain.entities import TaskStatus


class IntegrationResponseToDomainMapper:
    def map_one(self, data: IntegrationTaskDTO) -> TaskResultDTO:
        return TaskResultDTO(
            status=self._map_status(data.status),
            result=data.result.model_dump_json(),
            error=data.error
        )

    def _map_status(self, status: IntegrationTaskStatus) -> TaskStatus:
        if status == IntegrationTaskStatus.queued:
            return TaskStatus.queued
        elif status == IntegrationTaskStatus.started:
            return TaskStatus.started
        elif status == IntegrationTaskStatus.failed:
            return TaskStatus.failed
        elif status == IntegrationTaskStatus.finished:
            return TaskStatus.finished
        raise ValueError(f"Failed to map integration response: Unknown status {status}")
