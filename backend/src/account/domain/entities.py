from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Service(str, Enum):
    tiktok = "tiktok"
    youtube = "youtube"
    instagram = "instagram"


class AccountProfile(BaseModel):
    service: Service
    service_username: str

    model_config = ConfigDict(from_attributes=True)


class Account(BaseModel):
    id: UUID
    name: str
    profiles: list[AccountProfile]

    model_config = ConfigDict(from_attributes=True)


class AccountCreate(BaseModel):
    name: str


class AccountSearch(BaseModel):
    page: int
    count: int
    name: str | None = None


class AccountProfileCreate(BaseModel):
    account_id: UUID
    service: Service
    service_username: str
