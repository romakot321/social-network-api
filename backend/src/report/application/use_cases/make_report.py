import datetime
from uuid import UUID

from src.account.domain.entities import Service
from src.db.exceptions import DBModelNotFoundException
from src.integration.domain.entities import Video
from src.report.application.interfaces.task_adapter import IReportTaskAdapter
from src.report.domain.dtos import ReportMakeDTO
from src.report.domain.entities import Report
from src.task.domain.dtos import TaskListParamsDTO


class MakeReportUseCase:
    def __init__(self, task_adapter: IReportTaskAdapter):
        self.task_adapter = task_adapter

    async def execute(self, account_id: UUID, params: ReportMakeDTO) -> Report:
        return Report(
            from_datetime=params.from_datetime,
            to_datetime=params.to_datetime,
            youtube=await self.get_service_report(params.from_datetime, params.to_datetime, account_id, Service.youtube),
            tiktok=await self.get_service_report(params.from_datetime, params.to_datetime, account_id, Service.tiktok),
            instagram=await self.get_service_report(params.from_datetime, params.to_datetime, account_id, Service.instagram),
        )

    async def get_service_report(self, from_datetime, to_datetime, account_id, service: Service) -> Report.ServiceReport:
        from_datetime = from_datetime.replace(tzinfo=None)
        to_datetime = to_datetime.replace(tzinfo=None)
        try:
            task = await self.task_adapter.get_account_last(account_id, service)
        except DBModelNotFoundException:
            return Report.ServiceReport(view_count=0, video_count=0, average_views=0, top_video=None)
        videos = [v for v in task.items if from_datetime <= v.video_created_at <= to_datetime]

        view_count = sum(map(lambda i: i.view_count, videos))

        return Report.ServiceReport(
            view_count=view_count,
            video_count=len(videos),
            average_views=round(view_count / len(videos)) if videos else 0,
            top_video=max(map(lambda i: Video(**i.model_dump()), videos), key=lambda i: i.view_count) if videos else None,
        )
