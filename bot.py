import telebot
import json
import os

TOKEN = "8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74"
bot = telebot.TeleBot(TOKEN)

os.makedirs("data", exist_ok=True)

USERS_FILE = "data/users.json"
GROUPS_FILE = "data/groups.json"


def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@bot.message_handler(commands=['start'])
def start(message):
    users = load_data(USERS_FILE)
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.first_name or "",
            "username": message.from_user.username or "",
        }
        save_data(USERS_FILE, users)

    bot.reply_to(message, f"تم تسجيلك 👍\nعدد المستخدمين: {len(users)}")


@bot.message_handler(commands=['testdata'])
def testdata(message):
    users = load_data(USERS_FILE)
    bot.reply_to(message, f"البيانات الحالية:\n{users}")


@bot.message_handler(commands=['groups'])
def groups_count(message):
    groups = load_data(GROUPS_FILE)
    bot.reply_to(message, f"عدد الكروبات المخزنة: {len(groups)}")


@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def save_group(message):
    groups = load_data(GROUPS_FILE)
    group_id = str(message.chat.id)

    if group_id not in groups:
        groups[group_id] = {
            "title": message.chat.title or "",
        }
        save_data(GROUPS_FILE, groups)


print("Bot is running...")
bot.infinity_polling()
