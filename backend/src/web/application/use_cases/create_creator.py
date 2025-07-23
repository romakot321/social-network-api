from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.application.use_cases.add_account import AddAccountUseCase
from src.account.application.use_cases.add_account_profile import AddAccountProfileUseCase
from src.account.domain.dtos import AccountCreateDTO, AccountProfileCreateDTO, AccountReadDTO, AccountProfileReadDTO
from src.account.domain.entities import Service
from src.web.domain.dtos import CreatorCreateDTO


class CreateCreatorUseCase:
    def __init__(self, account_uow: IAccountUnitOfWork):
        self.account_uow = account_uow

    async def execute(self, dto: CreatorCreateDTO) -> AccountReadDTO:
        acc_create_dto = AccountCreateDTO(name=dto.name)
        account = await AddAccountUseCase(self.account_uow).execute(acc_create_dto)
        profiles = []

        if dto.youtube_username:
            profile_dto = AccountProfileCreateDTO(service=Service.youtube, service_username=dto.youtube_username)
            profiles.append(await AddAccountProfileUseCase(self.account_uow).execute(account.id, profile_dto))
        if dto.tiktok_username:
            profile_dto = AccountProfileCreateDTO(service=Service.tiktok, service_username=dto.tiktok_username)
            profiles.append(await AddAccountProfileUseCase(self.account_uow).execute(account.id, profile_dto))
        if dto.instagram_username:
            profile_dto = AccountProfileCreateDTO(service=Service.instagram, service_username=dto.instagram_username)
            profiles.append(await AddAccountProfileUseCase(self.account_uow).execute(account.id, profile_dto))
        if dto.fotobudka_url:
            service_username = dto.fotobudka_url.rsplit("/", 1)[-1]
            profile_dto = AccountProfileCreateDTO(service=Service.fotobudka, service_username=service_username)
            profiles.append(await AddAccountProfileUseCase(self.account_uow).execute(account.id, profile_dto))

        account.profiles = [AccountProfileReadDTO(**profile.model_dump()) for profile in profiles]

        return account
