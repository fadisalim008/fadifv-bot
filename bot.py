import telebot
import json
import os

bot = telebot.TeleBot("8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74")

os.makedirs("data", exist_ok=True)
DATA_FILE = "data/users.json"

def load_users():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

@bot.message_handler(commands=['start'])
def start(message):
    users = load_users()
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.first_name
        }
        save_users(users)

    bot.reply_to(message, "تم تسجيلك 👍")

bot.infinity_polling()
