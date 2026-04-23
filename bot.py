import telebot
import json

# 🔑 حط التوكن هنا
bot = telebot.TeleBot("8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74")

def load_users():
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=4)

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

# ▶️ تشغيل البوت
bot.infinity_polling()
