from src.integration.infrastructure.db.instagram_account_repository import PGInstagramAccountRepository
from src.db.engine import async_session_maker
from src.integration.infrastructure.scraper.instagram.entities import InstagramAccountCookies, InstagramPost
from src.integration.infrastructure.scraper.instagram.scraper import get_user_posts


class InstagramClient:
    def __init__(self, session_factory=async_session_maker) -> None:
        self.account_repository: PGInstagramAccountRepository = None
        self.session_factory = session_factory
        self.account: InstagramAccountCookies | None = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.account_repository = PGInstagramAccountRepository(self.session)
        self.account = await self.account_repository.get_random_cookies()
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()

    async def get_user_posts(self, username: str) -> list[InstagramPost]:
        if self.account is None:
            raise ValueError("Account not initalized")
        return await get_user_posts(username, self.account, "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0")
