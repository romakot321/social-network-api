import datetime

from pydantic import BaseModel


class ReportMakeDTO(BaseModel):
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime