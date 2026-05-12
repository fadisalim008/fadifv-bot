from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config import BOT_USERNAME, DEV_USERNAME

def source_button():
    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton(
            "SOURCE FADI",
            url=f"https://t.me/{DEV_USERNAME}"
        )
    )

    return kb

def start_buttons():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton(
            "اضفني للكروب",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
        )
    )

    kb.add(
        InlineKeyboardButton(
            "المطور",
            url=f"https://t.me/{DEV_USERNAME}"
        ),
        InlineKeyboardButton(
            "الاوامر",
            callback_data="help"
        )
    )

    return kb
