import asyncio
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from src.account.api.dependencies import get_account_uow, get_account_adapter
from src.account.application.use_cases.get_accounts_list import GetAccountsListUseCase
from src.account.domain.dtos import AccountListParamsDTO
from src.core.http.client import AsyncHttpClient
from src.task.api.dependencies import get_task_uow, get_report_task_adapter, get_task_runner
from src.web.application.use_cases.run_creator_scrap import RunCreatorScrapUseCase


@repeat_every(seconds=24 * 60 * 60, raise_exceptions=True)
async def scrape_accounts():
    account_uow = get_account_uow()
    task_uow = get_task_uow()
    task_runner = get_task_runner()
    account_adapter = get_account_adapter()

    accounts = await GetAccountsListUseCase(account_uow).execute(AccountListParamsDTO(count=99999999, page=0))
    for account in accounts:
        await RunCreatorScrapUseCase(task_uow, task_runner, account_adapter, AsyncHttpClient()).execute(account)
        await asyncio.sleep(30)
