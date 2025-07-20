from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from src.account.domain.entities import Service


class TaskStatus(str, Enum):
    queued = "queued"
    started = "started"
    failed = "failed"
    finished = "finished"


class Task(BaseModel):
    id: UUID
    status: TaskStatus
    account_id: UUID
    service: Service
    result: str | None = None
    error: str | None = None


class TaskCreate(BaseModel):
    account_id: UUID
    service: Service


class TaskRun(BaseModel):
    service: Service
    username: str


class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    result: str | None = None
    error: str | None = None
