from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.config import Config


async def register(app):
    
    @app.on_message(filters.command("start"))
    async def start_handler(client, message):

        text = (
            "𖣂\n\n"
            "- أهلاً بك في بوت الحماية.\n"
            "- وظيفتي حماية المجموعات من التخريب والتفلش.\n"
            "- لتفعيل البوت أرسل كلمة: تفعيل"
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "اضفني",
                        url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true"
                    ),
                    InlineKeyboardButton(
                        "المطور",
                        url=f"https://t.me/{Config.OWNER_USERNAME}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "شراء بوت مشابه",
                        url=f"https://t.me/{Config.OWNER_USERNAME}"
                    )
                ]
            ]
        )

        await message.reply_text(
            text,
            reply_markup=keyboard
        )
