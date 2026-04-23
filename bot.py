from telebot import TeleBot
import json
import os

TOKEN = "8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74"

bot = TeleBot(TOKEN)

USERS_FILE = "data/users.json"
GROUPS_FILE = "data/groups.json"

# تحميل البيانات
def load_data(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

# حفظ البيانات
def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# تسجيل مستخدم
def save_user(user_id):
    data = load_data(USERS_FILE)
    data[str(user_id)] = True
    save_data(USERS_FILE, data)

# تسجيل كروب
def save_group(chat_id):
    data = load_data(GROUPS_FILE)
    data[str(chat_id)] = True
    save_data(GROUPS_FILE, data)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == "private":
        save_user(message.from_user.id)
    else:
        save_group(message.chat.id)

    bot.reply_to(message, "بوتك شغال ويخزن البيانات بنجاح 🔥")

print("Bot running...")
bot.infinity_polling()
