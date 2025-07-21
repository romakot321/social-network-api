import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.account.domain.entities import Service


class TaskStatus(str, Enum):
    queued = "queued"
    started = "started"
    failed = "failed"
    finished = "finished"


class TaskItem(BaseModel):
    id: UUID
    task_id: UUID
    url: str
    thumbnail_url: str
    view_count: int
    title: str | None = None
    description: str | None = None
    video_created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class Task(BaseModel):
    id: UUID
    status: TaskStatus
    account_id: UUID
    service: Service
    items: list[TaskItem]
    error: str | None = None


class TaskItemCreate(BaseModel):
    task_id: UUID
    url: str
    thumbnail_url: str
    view_count: int
    title: str | None = None
    description: str | None = None
    video_created_at: datetime.datetime


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
