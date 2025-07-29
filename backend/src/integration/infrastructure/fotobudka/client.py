import datetime

from src.core.config import settings
from src.core.http.client import IHttpClient
from src.integration.infrastructure.http_api_client import HttpApiClient
from src.integration.infrastructure.fotobudka.schemas import FotobudkaPartnerStatResponse

_cache = {}


class FotobudkaClient(HttpApiClient):
    def __init__(self, client: IHttpClient, source_url="https://bot.fotobudka.online"):
        super().__init__(client, source_url=source_url, token=settings.FOTOBUDKA_API_TOKEN)

    async def get_partner_stat(self, partner_code: str) -> FotobudkaPartnerStatResponse:
        if (cached := _cache.get(partner_code)) is not None:
            schema, created_at = cached
            if (datetime.datetime.now() - created_at).seconds <= 24 * 60 * 60:
                return schema

        response = await self.request("GET", "/api/v1/partnerStat", params={"partnerCode": partner_code}, headers={"Authorization": "Bearer f113066f-2ad6-43eb-b860-8683fde1042a"})
        schema = self.validate_response(response.data, FotobudkaPartnerStatResponse)
        _cache[partner_code] = (schema, datetime.datetime.now())
        return schema
