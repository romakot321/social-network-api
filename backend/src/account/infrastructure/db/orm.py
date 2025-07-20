from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import BaseMixin, Base


class AccountDB(BaseMixin, Base):
    __tablename__ = "accounts"

    name: Mapped[str]

    profiles: Mapped[list["AccountProfileDB"]] = relationship(back_populates="account", lazy="selectin")


class AccountProfileDB(BaseMixin, Base):
    __tablename__ = "account_profiles"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    service: Mapped[str]
    service_username: Mapped[str]

    account: Mapped["AccountDB"] = relationship(back_populates="profiles", lazy="noload")