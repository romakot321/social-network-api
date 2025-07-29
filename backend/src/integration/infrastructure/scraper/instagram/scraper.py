import json
import asyncio
import httpx
from urllib.parse import quote

from src.integration.infrastructure.scraper.instagram.entities import InstagramAccountCookies, InstagramPost

headers = {
    "x-ig-app-id": "936619743392459",
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "*/*",
    "X-ASBD-ID": "359341",
    "X-BLOKS-VERSION-ID": "4fd52d0e0985dd463fefe21d18f1609258ecf3c799cc7f12f6c4363b56697384",
    "X-FB-Friendly-Name": "PolarisProfilePostsTabContentQuery_connection",
    "X-FB-LSD": "NlPIl85YkYcS0hoerPjXRz",
    "X-Root-Field-Name": 'xdt_api__v1__feed__user_timeline_graphql_connection'
}

INSTAGRAM_ACCOUNT_DOCUMENT_ID = "30714410208142251"
PAGE_FETCH_SLEEP = 5
POST_FETCH_SLEEP = 1


async def scrape_user_posts(session, username: str, page_size=12, max_pages: int | None = None):
    base_url = "https://www.instagram.com/graphql/query"
    variables = {
        "after": None,
        "before": None,
        "data": {
            "count": page_size,
            "include_reel_media_seen_timestamp": True,
            "include_relationship_info": True,
            "latest_besties_reel_media": True,
            "latest_reel_media": True
        },
        "first": page_size,
        "last": None,
        "username": f"{username}",
        "__relay_internal__pv__PolarisIsLoggedInrelayprovider": True,
        "__relay_internal__pv__PolarisShareSheetV3relayprovider": True,
    }

    prev_cursor = None
    _page_number = 1

    while True:
        body = f"variables={quote(json.dumps(variables, separators=(',', ':')))}&doc_id={INSTAGRAM_ACCOUNT_DOCUMENT_ID}"

        response = await session.post(
            base_url, data=body, headers={"content-type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        data = response.json()

        with open("ts2.json", "a", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        posts = data["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]
        for post in posts["edges"]:
            yield post["node"]

        page_info = posts["page_info"]
        if not page_info["has_next_page"]:
            print(f"scraping posts page {_page_number}")
            break

        if page_info["end_cursor"] == prev_cursor:
            print("found no new posts, breaking")
            break

        prev_cursor = page_info["end_cursor"]
        variables["after"] = page_info["end_cursor"]
        _page_number += 1

        if max_pages and _page_number > max_pages:
            break

        await asyncio.sleep(PAGE_FETCH_SLEEP)


async def scrape_user(session, username: str):
    """Scrape Instagram user's data"""
    result = await session.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
    )
    data = result.json()
    # print(data)
    return data["data"]["user"]


async def get_user_posts(username: str, cookies: InstagramAccountCookies, user_agent: str) -> list[InstagramPost]:
    posts = []
    headers["X-CSRFToken"] = cookies.csrftoken
    headers["User-Agent"] = user_agent

    async with httpx.AsyncClient(timeout=httpx.Timeout(20.0), headers=headers, cookies=cookies.model_dump()) as session:
        async for post in scrape_user_posts(session, username):
            await asyncio.sleep(POST_FETCH_SLEEP)
            resp = await session.get(f"https://www.instagram.com/api/v1/media/{post['pk']}/info/", follow_redirects=True)
            resp.raise_for_status()
            post_info = resp.json()['items'][0]
            posts.append(InstagramPost.model_validate(post_info))

    return posts
