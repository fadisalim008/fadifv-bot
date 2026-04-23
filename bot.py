import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8516176029:AAH-s3Y0nLAdmQN_LyeR3aS-tbK1XInMINY"

BOT_USERNAME = "fadifvambot"
DEV_USERNAME = "fvamv"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{DEV_USERNAME}")
    btn2 = InlineKeyboardButton("➕ اضفني للكروب", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
    btn3 = InlineKeyboardButton("💰 شراء بوت مشابه", url=f"https://t.me/{DEV_USERNAME}")

    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)

    bot.send_message(
        message.chat.id,
        "أهلاً بك في بوت فادي المطور 🌷\nاختر من الأزرار بالأسفل 👇",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: True)
def reply_all(message):
    if message.text == "سورس":
        bot.reply_to(message, "أهلاً بك في سورس فادي 🔥")

bot.infinity_polling()
