import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.integration.infrastructure.fotobudka.client import FotobudkaClient
from src.core.http.client import AsyncHttpClient

from src.account.application.use_cases.add_account import AddAccountUseCase
from src.account.application.use_cases.get_account import GetAccountUseCase
from src.account.application.use_cases.get_accounts_list import GetAccountsListUseCase
from src.account.domain.dtos import AccountListParamsDTO, AccountCreateDTO
from src.report.application.use_cases.make_report import MakeReportUseCase
from src.report.domain.dtos import ReportMakeDTO
from src.task.api.dependencies import HttpClientDepend, AccountAdapterDepend, TaskRunnerDepend
from src.web.api.dependencies import AccountUoWDepend, TaskUoWDepend, ReportTaskAdapterDepend
from src.web.application.use_cases.create_creator import CreateCreatorUseCase
from src.web.application.use_cases.get_creator_videos import GetCreatorVideosUseCase
from src.web.application.use_cases.get_creators_list import GetCreatorsListUseCase
from src.web.application.use_cases.run_creator_scrap import RunCreatorScrapUseCase
from src.web.domain.dtos import CreatorCreateDTO, CreatorVideosListParamsDTO, CreatorReadDTO

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def creators_list_page(
    request: Request, account_uow: AccountUoWDepend, task_uow: TaskUoWDepend, params: AccountListParamsDTO = Depends()
):
    fotobudka_client = FotobudkaClient(AsyncHttpClient())
    creators = await GetCreatorsListUseCase(task_uow, account_uow, fotobudka_client).execute(params)
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "creators": creators,
            "params": params,
            "dates": {
                "today_start": today,
                "today_end": today.replace(hour=23, minute=59, second=59),
                "yesterday_start": today - datetime.timedelta(days=1),
                "yesterday_end": (today - datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59),
                "current_month_start": today.replace(day=1),
                "current_month_end": ((today.replace(day=1, month=today.month + 1)) - datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59),
                "previous_month_start": today.replace(day=1, month=today.month - 1),
                "previous_month_end": (today.replace(day=1) - datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59),
                "all_time_end": today.replace(hour=23, minute=59, second=59),
            },
        },
    )


@router.get("/creator/{account_id}", response_class=HTMLResponse)
async def creator_details_page(
    request: Request,
    account_uow: AccountUoWDepend,
    task_adapter: ReportTaskAdapterDepend,
    task_uow: TaskUoWDepend,
    account_id: UUID,
    dto: CreatorVideosListParamsDTO = Depends(),
):
    account = await GetAccountUseCase(account_uow).execute(account_id)
    videos = await GetCreatorVideosUseCase(task_uow).execute(account_id, dto)
    from_datetime = datetime.datetime.now()
    report = await MakeReportUseCase(task_adapter).execute(
        account_id,
        ReportMakeDTO(
            from_datetime=from_datetime,
            to_datetime=datetime.datetime.now() - datetime.timedelta(days=from_datetime.weekday()),
        ),
    )
    return templates.TemplateResponse(
        "creator.html", {"request": request, "account": account, "videos": videos, "report": report}
    )


@router.get("/create", response_class=HTMLResponse)
async def creator_create_page(request: Request):
    return templates.TemplateResponse("add_creator.html", {"request": request})


@router.post("/create", response_class=HTMLResponse)
async def create_creator(
    account_uow: AccountUoWDepend,
    task_uow: TaskUoWDepend,
    http_client: HttpClientDepend,
    account_adapter: AccountAdapterDepend,
    runner: TaskRunnerDepend,
    dto: CreatorCreateDTO = Depends(CreatorCreateDTO.as_form),
):
    account = await CreateCreatorUseCase(account_uow).execute(dto)
    await RunCreatorScrapUseCase(task_uow, runner, account_adapter, http_client).execute(account)
    return RedirectResponse(url="/", status_code=303)
