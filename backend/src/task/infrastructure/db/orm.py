import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from src.db.base import Base, BaseMixin


class TaskItemDB(BaseMixin, Base):
    __tablename__ = "task_item"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    url: Mapped[str]
    thumbnail_url: Mapped[str]
    view_count: Mapped[int]
    title: Mapped[str | None]
    description: Mapped[str | None]
    video_created_at: Mapped[datetime.datetime]

    task: Mapped["TaskDB"] = relationship(back_populates="items")


class TaskDB(BaseMixin, Base):
    __tablename__ = "tasks"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    service: Mapped[str]
    status: Mapped[str | None]
    error: Mapped[str | None]

    items: Mapped[list["TaskItemDB"]] = relationship(back_populates="task", lazy="selectin")
