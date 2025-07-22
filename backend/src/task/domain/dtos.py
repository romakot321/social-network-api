import datetime
import inspect
from typing import Type
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel, HttpUrl, ConfigDict

from src.account.domain.entities import Service
from src.task.domain.entities import TaskStatus


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.model_fields.items():
        new_parameters.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...) if model_field.is_required() else Form(model_field.default),
                annotation=model_field.annotation,
            )
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    cls.as_form = as_form_func
    return cls


@as_form
class TaskCreateDTO(BaseModel):
    account_id: UUID
    service: Service
    webhook_url: HttpUrl | None = None

    @classmethod
    def as_form(cls): ...


class TaskItemReadDTO(BaseModel):
    url: str
    thumbnail_url: str
    view_count: int
    title: str | None = None
    description: str | None = None
    video_created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class TaskReadResultDTO(BaseModel):
    id: UUID
    status: TaskStatus
    items: list[TaskItemReadDTO]
    error: str | None = None


class TaskReadDTO(BaseModel):
    id: UUID
    status: TaskStatus
    items: list[TaskItemReadDTO]
    error: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskResultDTO(BaseModel):
    status: TaskStatus
    items: list[TaskItemReadDTO]
    error: str | None = None


class TaskListParamsDTO(BaseModel):
    from_created_at: datetime.datetime | None = None
    to_created_at: datetime.datetime | None = None
    from_video_created_at: datetime.datetime | None = None
    to_video_created_at: datetime.datetime | None = None
    account_id: UUID | None = None
    service: Service | None = None
