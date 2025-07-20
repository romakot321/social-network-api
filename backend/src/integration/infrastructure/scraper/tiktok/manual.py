import asyncio

from src.integration.infrastructure.scraper.tiktok.bot import TikTokPy


async def main():
    async with TikTokPy() as bot:
        # 😏 getting user's feed
        user_feed_items = await bot.user_feed(username="tiktok_russia", amount=1)
        print(user_feed_items[0].author_stats)
        user_feed_items = await bot.user_feed(username="tiktok_russia", amount=user_feed_items[0].author_stats.videos)
        for item in user_feed_items:
            print("Music title: ", item.music.title)
            print([tag.title for tag in item.challenges])
            print("Comments: ", item.stats.comments)
            print("Plays: ", item.stats.plays)
            print("Shares: ", item.stats.shares)
            print("Likes: ", item.stats.likes)

        # and many other things 😉


if __name__ == "__main__":
    asyncio.run(main())
