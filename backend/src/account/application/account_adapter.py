from uuid import UUID

from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.application.use_cases.get_account_profiles_list import GetAccountProfilesListUseCase
from src.account.domain.entities import Service
from src.task.application.interfaces.task_account_adapter import ITaskAccountAdapter


class AccountAdapter(ITaskAccountAdapter):
    def __init__(self, uow: IAccountUnitOfWork):
        self.uow = uow

    async def get_account_profile_username(self, account_id: UUID, service: Service) -> str | None:
        profiles = await GetAccountProfilesListUseCase(self.uow).execute(account_id)
        for profile in profiles:
            if profile.service == service:
                return profile.service_username
        return None
