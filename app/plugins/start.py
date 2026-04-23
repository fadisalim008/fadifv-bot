from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config import Config


def register(app):

    @app.on_message(filters.command("start"))
    async def start_handler(client, message):
        text = (
            "🌿 أهلاً بك في بوت الحماية\n"
            "- أرسل كلمة: الاوامر\n"
            "- حتى تظهر لك الأقسام"
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "اضفني",
                        url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "المطور",
                        url=f"https://t.me/{Config.OWNER_USERNAME}"
                    ),
                    InlineKeyboardButton(
                        "شراء البوت",
                        url=f"https://t.me/{Config.OWNER_USERNAME}"
                    )
                ]
            ]
        )

        await message.reply_text(text, reply_markup=keyboard)
