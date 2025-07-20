from enum import Enum

from pydantic import BaseModel

from src.account.domain.entities import Service
from src.integration.domain.entities import Video


class IntegrationTaskStatus(str, Enum):
    queued = "queued"
    started = "started"
    finished = "finished"
    failed = "failed"


class IntegrationTaskRunParamsDTO(BaseModel):
    prompt: str


class IntegrationTaskResultDTO(BaseModel):
    service: Service
    username: str
    videos: list[Video]


class IntegrationTaskDTO(BaseModel):
    status: IntegrationTaskStatus
    result: IntegrationTaskResultDTO | None = None
    error: str | None = None
