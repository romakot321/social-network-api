from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.db.base import Base, BaseMixin


class TaskDB(BaseMixin, Base):
    __tablename__ = "tasks"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    service: Mapped[str]
    status: Mapped[str | None]
    result: Mapped[str | None]
    error: Mapped[str | None]
