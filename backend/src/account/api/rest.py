from fastapi import APIRouter

from src.account.api.dependencies import AccountUoWDepend
from src.account.application.use_cases.add_account import AddAccountUseCase
from src.account.application.use_cases.get_accounts_list import GetAccountsListUseCase
from src.account.domain.dtos import AccountReadDTO, AccountCreateDTO, AccountListParamsDTO

router = APIRouter()


@router.post("", response_model=AccountReadDTO)
async def create_account(uow: AccountUoWDepend, dto: AccountCreateDTO):
    return await AddAccountUseCase(uow).execute(dto)


@router.get("", response_model=list[AccountReadDTO])
async def get_accounts_list(uow: AccountUoWDepend, dto: AccountListParamsDTO):
    return await GetAccountsListUseCase(uow).execute(dto)