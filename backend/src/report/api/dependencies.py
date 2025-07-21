from typing import Annotated

from fastapi import Depends

from src.report.application.interfaces.task_adapter import IReportTaskAdapter
from src.task.api.dependencies import get_report_task_adapter

TaskAdapterDepend = Annotated[IReportTaskAdapter, Depends(get_report_task_adapter)]