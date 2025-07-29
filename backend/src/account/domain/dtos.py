import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.account.domain.entities import Service


class AccountProfileReadDTO(BaseModel):
    service: Service
    service_username: str

    model_config = ConfigDict(from_attributes=True)


class AccountReadDTO(BaseModel):
    id: UUID
    name: str
    profiles: list[AccountProfileReadDTO]

    model_config = ConfigDict(from_attributes=True)


class AccountCreateDTO(BaseModel):
    name: str


class AccountProfileCreateDTO(BaseModel):
    service: Service
    service_username: str


class AccountListParamsDTO(BaseModel):
    page: int = 0
    count: int = 100
    name: str | None = None
    stats_from: datetime.datetime | None = None
    stats_to: datetime.datetime | None = None
