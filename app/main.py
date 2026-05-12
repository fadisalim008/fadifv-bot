from telebot import TeleBot
from telebot.types import Message

from app.config import BOT_TOKEN
from app.buttons import start_buttons
from app.music import send_music
from app.weather import get_weather
from app.ai import ask_ai
from app.games import (
    make_game,
    handle_game_answer,
    start_fast,
    check_fast
)

bot = TeleBot(BOT_TOKEN, parse_mode="HTML")


@bot.message_handler(commands=["start"])
def start(message: Message):

    bot.send_message(
        message.chat.id,
        "هلا بك في بوت فادي",
        reply_markup=start_buttons()
    )


@bot.message_handler(func=lambda m: m.text and m.text.startswith("يوت "))
def music(message: Message):

    query = message.text.replace("يوت ", "")

    send_music(bot, message, query)


@bot.message_handler(func=lambda m: m.text and m.text.startswith("طقس "))
def weather(message: Message):

    city = message.text.replace("طقس ", "")

    bot.reply_to(
        message,
        get_weather(city)
    )


@bot.message_handler(func=lambda m: m.text and m.text.startswith("زنجي "))
def ai(message: Message):

    q = message.text.replace("زنجي ", "")

    bot.reply_to(
        message,
        ask_ai(q)
    )


@bot.message_handler(func=lambda m: m.text in [
    "لغز",
    "اعلام",
    "رياضيات",
    "عربي",
    "انكليزي",
    "عواصم",
    "سيارات",
    "مشاهير",
    "كلمات",
    "دين",
    "بات",
    "امثله",
    "انمي",
    "المختلف",
    "العكس"
])
def games(message: Message):

    q, kb = make_game(message.text)

    bot.send_message(
        message.chat.id,
        q,
        reply_markup=kb
    )


@bot.message_handler(func=lambda m: m.text == "الاسرع")
def fast(message: Message):

    word = start_fast(message.chat.id)

    bot.send_message(
        message.chat.id,
        f"اول واحد يكتب:\n{word}"
    )


@bot.message_handler(func=lambda m: m.text)
def fast_check(message: Message):

    if check_fast(message.chat.id, message.text):

        bot.reply_to(
            message,
            "✅ فزت"
        )


@bot.callback_query_handler(func=lambda c: c.data.startswith("game:"))
def game_answer(call):

    handle_game_answer(bot, call)


print("BOT STARTED")

bot.infinity_polling()
