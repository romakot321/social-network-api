from uuid import UUID

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.account.application.use_cases.add_account import AddAccountUseCase
from src.account.application.use_cases.get_account import GetAccountUseCase
from src.account.application.use_cases.get_accounts_list import GetAccountsListUseCase
from src.account.domain.dtos import AccountListParamsDTO, AccountCreateDTO
from src.task.api.dependencies import HttpClientDepend, AccountAdapterDepend, TaskRunnerDepend
from src.web.api.dependencies import AccountUoWDepend, TaskUoWDepend
from src.web.application.use_cases.create_creator import CreateCreatorUseCase
from src.web.application.use_cases.get_creator_videos import GetCreatorVideosUseCase
from src.web.application.use_cases.get_creators_list import GetCreatorsListUseCase
from src.web.application.use_cases.run_creator_scrap import RunCreatorScrapUseCase
from src.web.domain.dtos import CreatorCreateDTO

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def creators_list_page(request: Request, account_uow: AccountUoWDepend, task_uow: TaskUoWDepend, params: AccountListParamsDTO = Depends()):
    creators = await GetCreatorsListUseCase(task_uow, account_uow).execute(params)
    return templates.TemplateResponse("index.html", {"request": request, "creators": creators})


@router.get("/creator/{account_id}", response_class=HTMLResponse)
async def creator_details_page(request: Request, account_uow: AccountUoWDepend, task_uow: TaskUoWDepend, account_id: UUID):
    account = await GetAccountUseCase(account_uow).execute(account_id)
    videos = await GetCreatorVideosUseCase(task_uow).execute(account_id)
    return templates.TemplateResponse("creator.html", {"request": request, "account": account, "videos": videos})


@router.get("/create", response_class=HTMLResponse)
async def creator_create_page(request: Request):
    return templates.TemplateResponse("add_creator.html", {"request": request})


@router.post("/create", response_class=HTMLResponse)
async def create_creator(account_uow: AccountUoWDepend, task_uow: TaskUoWDepend,
        http_client: HttpClientDepend,
        account_adapter: AccountAdapterDepend,
        runner: TaskRunnerDepend, dto: CreatorCreateDTO = Depends(CreatorCreateDTO.as_form)):
    account = await CreateCreatorUseCase(account_uow).execute(dto)
    await RunCreatorScrapUseCase(task_uow, runner, account_adapter, http_client).execute(account)
    return RedirectResponse(url="/", status_code=303)