import abc
from uuid import UUID

from src.account.domain.entities import Service


class ITaskAccountAdapter(abc.ABC):
    @abc.abstractmethod
    async def get_account_profile_username(self, account_id: UUID, service: Service) -> str: ...
