import telebot
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74"
CHANNEL_USERNAME = "@fadifva"   # حط يوزر قناتك
OWNER_ID = 8065884629            # حط ايديك الرقمي هنا

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


def save_user(message):
    users = load_data(USERS_FILE)
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.first_name or "",
            "username": message.from_user.username or ""
        }
        save_data(USERS_FILE, users)


def save_group(message):
    if message.chat.type in ["group", "supergroup"]:
        groups = load_data(GROUPS_FILE)
        group_id = str(message.chat.id)

        if group_id not in groups:
            groups[group_id] = {
                "title": message.chat.title or ""
            }
            save_data(GROUPS_FILE, groups)


def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


def join_channel_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("اشترك بالقناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")
    )
    return markup


def require_subscription(message):
    if not is_subscribed(message.from_user.id):
        bot.reply_to(
            message,
            f"لازم تشترك بقناتنا أولًا حتى تستخدم البوت:\n{CHANNEL_USERNAME}",
            reply_markup=join_channel_markup()
        )
        return False
    return True


@bot.message_handler(commands=['start'])
def start(message):
    save_user(message)
    save_group(message)

    if not require_subscription(message):
        return

    users = load_data(USERS_FILE)
    bot.reply_to(
        message,
        f"هلا {message.from_user.first_name} 🌷\n"
        f"تم تسجيلك بنجاح\n"
        f"عدد المستخدمين الحالي: {len(users)}"
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    save_user(message)
    save_group(message)

    if not require_subscription(message):
        return

    text = (
        "أوامر البوت:\n\n"
        "/start - بدء البوت\n"
        "/help - عرض الأوامر\n"
        "/stats - إحصائيات البوت (للمالك فقط)\n"
        "/users - عدد المستخدمين (للمالك فقط)\n"
        "/groups - عدد الكروبات (للمالك فقط)\n"
        "/broadcast - إذاعة للكل (للمالك فقط)\n"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != OWNER_ID:
        return

    users = load_data(USERS_FILE)
    groups = load_data(GROUPS_FILE)

    bot.reply_to(
        message,
        f"إحصائيات البوت:\n\n"
        f"عدد المستخدمين: {len(users)}\n"
        f"عدد الكروبات: {len(groups)}"
    )


@bot.message_handler(commands=['users'])
def users_command(message):
    if message.from_user.id != OWNER_ID:
        return

    users = load_data(USERS_FILE)
    bot.reply_to(message, f"عدد المستخدمين: {len(users)}")


@bot.message_handler(commands=['groups'])
def groups_command(message):
    if message.from_user.id != OWNER_ID:
        return

    groups = load_data(GROUPS_FILE)
    bot.reply_to(message, f"عدد الكروبات: {len(groups)}")


@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != OWNER_ID:
        return

    text = message.text.replace("/broadcast", "", 1).strip()

    if not text:
        bot.reply_to(message, "اكتب الرسالة هيج:\n/broadcast اهلاً بالجميع")
        return

    users = load_data(USERS_FILE)
    sent = 0

    for user_id in users:
        try:
            bot.send_message(int(user_id), text)
            sent += 1
        except:
            pass

    bot.reply_to(message, f"تم إرسال الإذاعة إلى {sent} مستخدم")


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
    save_group(message)

    for user in message.new_chat_members:
        try:
            text = (
                f"هلا {user.first_name} 🌷\n"
                f"نورت الكروب: {message.chat.title}\n"
                f"التزم بالقوانين وتقدر تشارك برأيك بكل احترام."
            )
            bot.send_message(message.chat.id, text)
        except:
            pass


@bot.message_handler(func=lambda message: True)
def all_messages(message):
    save_user(message)
    save_group(message)

    if message.chat.type == "private":
        if not require_subscription(message):
            return


print("Bot is running...")
bot.infinity_polling()
