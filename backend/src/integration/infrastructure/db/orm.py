from sqlalchemy.orm import Mapped
from src.db.base import Base, BaseMixin


class InstagramAccountDB(BaseMixin, Base):
    __tablename__ = "instagram_accounts"

    email: Mapped[str]
    cookies: Mapped[str]
