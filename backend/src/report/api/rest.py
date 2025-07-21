from uuid import UUID

from fastapi import APIRouter

from src.report.api.dependencies import TaskAdapterDepend
from src.report.application.use_cases.make_report import MakeReportUseCase
from src.report.domain.dtos import ReportMakeDTO
from src.report.domain.entities import Report

router = APIRouter()


@router.post("/account/{account_id}", response_model=Report)
async def make_account_report(task_adapter: TaskAdapterDepend, account_id: UUID, params: ReportMakeDTO):
    return await MakeReportUseCase(task_adapter).execute(account_id, params)