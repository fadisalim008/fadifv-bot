import asyncio
import logging
from pyrogram import Client, idle
from pyrogram.enums import ParseMode

from app.config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

LOGGER = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        self.app = Client(
            "bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            parse_mode=ParseMode.HTML
        )

    async def start(self):
        LOGGER.info("Starting bot...")
        await self.app.start()

        me = await self.app.get_me()
        LOGGER.info(f"Bot started as @{me.username}")

        await idle()

    async def stop(self):
        LOGGER.info("Stopping bot...")
        await self.app.stop()


async def main():
    bot = Bot()
    try:
        await bot.start()
    except Exception as e:
        LOGGER.exception(e)
    finally:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
