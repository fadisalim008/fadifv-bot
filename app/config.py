import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

BOT_USERNAME = os.getenv("BOT_USERNAME", "")

DEV_USERNAME = os.getenv("DEV_USERNAME", "fvamv")

FORCE_CHANNEL = os.getenv("FORCE_CHANNEL", "fadifva")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

RAPID_API_KEY = os.getenv("RAPID_API_KEY", "")

START_PHOTO = os.getenv(
    "START_PHOTO",
    "https://i.ibb.co/xqVzNV7t/db72f6d6-2b6a-4f58-abdc-2f47a3aeb664.jpg"
)
