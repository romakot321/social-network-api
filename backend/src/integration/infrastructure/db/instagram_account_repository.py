from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.exceptions import DBModelNotFoundException
from src.integration.infrastructure.db.orm import InstagramAccountDB
from src.integration.infrastructure.scraper.instagram.entities import InstagramAccountCookies


class PGInstagramAccountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_random_cookies(self) -> InstagramAccountCookies:
        query = select(InstagramAccountDB).order_by(func.random()).limit(1)
        model = await self.session.scalar(query)
        if model is None:
            raise DBModelNotFoundException()
        return InstagramAccountCookies.model_validate_json(model.cookies)
