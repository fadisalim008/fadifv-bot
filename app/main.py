import asyncio
from pyrogram import Client, idle
from app.config import Config
from app.loader import load_plugins


async def main():
    app = Client(
        "Aurelius",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN
    )

    await app.start()
    print("Bot Started 🔥")

    await load_plugins(app)

    await idle()


if __name__ == "__main__":
    asyncio.run(main())
