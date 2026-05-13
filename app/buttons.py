import requests
from app.config import BOT_TOKEN, BOT_USERNAME, DEV_USERNAME

def blue_btn(text, callback_data=None, url=None):
    b = {"text": text, "style": "primary"}
    if callback_data:
        b["callback_data"] = callback_data
    if url:
        b["url"] = url
    return b

def red_btn(text, callback_data=None, url=None):
    b = {"text": text, "style": "danger"}
    if callback_data:
        b["callback_data"] = callback_data
    if url:
        b["url"] = url
    return b

def source_button():
    return {
        "inline_keyboard": [
            [red_btn("SOURCE FADI", url=f"https://t.me/{DEV_USERNAME}")]
        ]
    }

def start_buttons():
    return {
        "inline_keyboard": [
            [blue_btn("اضفني للكروب", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                blue_btn("المطور", url=f"https://t.me/{DEV_USERNAME}"),
                blue_btn("الاوامر", callback_data="help")
            ],
            [red_btn("SOURCE FADI", url=f"https://t.me/{DEV_USERNAME}")]
        ]
    }

def raw_send_photo(chat_id, photo, caption, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "photo": photo,
        "caption": caption,
        "parse_mode": "HTML"
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    return requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        json=payload,
        timeout=20
    ).json()
