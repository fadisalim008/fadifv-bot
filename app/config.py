import os

class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    BOT_USERNAME = os.getenv("BOT_USERNAME")
    OWNER_USERNAME = os.getenv("OWNER_USERNAME")
