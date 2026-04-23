import telebot
from telebot import types
import json
import os
import re
from datetime import datetime

BOT_TOKEN = "8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74"
BOT_USERNAME = "Fadifvbot"
DEV_USERNAME = "fvamv"
CHANNEL_USERNAME = "fadifva"
OWNER_ID = 8065884629  # حط ايديك هنا

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# =========================
# ملفات الداتا
# =========================
if not os.path.exists("data"):
    os.makedirs("data")

FILES = {
    "users": "data/users.json",
    "groups": "data/groups.json",
    "ranks": "data/ranks.json"
}

for path in FILES.values():
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_users():
    return load_json(FILES["users"])


def save_users(data):
    save_json(FILES["users"], data)


def load_groups():
    return load_json(FILES["groups"])


def save_groups(data):
    save_json(FILES["groups"], data)


def load_ranks():
    return load_json(FILES["ranks"])


def save_ranks(data):
    save_json(FILES["ranks"], data)


# =========================
# الداتا الافتراضية
# =========================
DEFAULT_LOCKS = {
    "links": False,
    "photos": False,
    "videos": False,
    "stickers": False,
    "forwards": False,
    "bots": False,
    "chat": False,
    "usernames": False,
}

DEFAULT_GROUP = {
    "welcome_enabled": False,
    "welcome_text": "اهلاً {name} نورت {group} 🌿",
    "rules": "",
    "description": "",
    "locks": DEFAULT_LOCKS.copy(),
    "warns": {},
    "muted": [],
    "banned": []
}


def ensure_user(user):
    users = load_users()
    uid = str(user.id)
    if uid not in users:
        users[uid] = {
            "name": user.first_name or "",
            "username": user.username or ""
        }
        save_users(users)


def ensure_group(chat):
    groups = load_groups()
    gid = str(chat.id)

    if gid not in groups:
        groups[gid] = {
            "welcome_enabled": False,
            "welcome_text": "اهلاً {name} نورت {group} 🌿",
            "rules": "",
            "description": "",
            "locks": DEFAULT_LOCKS.copy(),
            "warns": {},
            "muted": [],
            "banned": []
        }
        save_groups(groups)

    ranks = load_ranks()
    if gid not in ranks:
        ranks[gid] = {
            "owners": [],
            "admins_local": [],
            "vips": []
        }
        save_ranks(ranks)


def get_group_data(chat_id):
    groups = load_groups()
    return groups.get(str(chat_id), DEFAULT_GROUP.copy())


# =========================
# أدوات
# =========================
def is_group(message):
    return message.chat.type in ["group", "supergroup"]


def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


def force_sub(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📢 اشترك بالقناة", url=f"https://t.me/{CHANNEL_USERNAME}")
    )
    bot.reply_to(
        message,
        f"🚀 لازم تشترك بالقناة حتى تستخدم البوت:\nhttps://t.me/{CHANNEL_USERNAME}",
        reply_markup=markup
    )


def is_telegram_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False


def get_local_rank(chat_id, user_id):
    ranks = load_ranks()
    gid = str(chat_id)
    uid = str(user_id)

    if gid not in ranks:
        return None
    if uid in ranks[gid].get("owners", []):
        return "owner"
    if uid in ranks[gid].get("admins_local", []):
        return "admin"
    if uid in ranks[gid].get("vips", []):
        return "vip"
    return None


def has_admin_power(chat_id, user_id):
    if is_telegram_admin(chat_id, user_id):
        return True
    return get_local_rank(chat_id, user_id) in ["owner", "admin"]


def has_owner_power(chat_id, user_id):
    if is_telegram_admin(chat_id, user_id):
        return True
    return get_local_rank(chat_id, user_id) == "owner"


def mention(user):
    name = getattr(user, "first_name", None) or str(user.id)
    return f"<a href='tg://user?id={user.id}'>{name}</a>"


def get_target_user(message):
    if message.reply_to_message:
        return message.reply_to_message.from_user

    parts = (message.text or "").split()
    if len(parts) >= 2 and parts[1].isdigit():
        class TempUser:
            def __init__(self, uid):
                self.id = int(uid)
                self.first_name = str(uid)
        return TempUser(parts[1])

    return None


def protected_target(chat_id, user_id):
    if is_telegram_admin(chat_id, user_id):
        return True
    return get_local_rank(chat_id, user_id) in ["owner", "admin"]


def admin_only(message):
    bot.reply_to(message, "❌ هذا الأمر فقط للمشرف وفوك.")


def owner_only(message):
    bot.reply_to(message, "❌ هذا الأمر فقط للمالك.")


def mute_permissions():
    return types.ChatPermissions(can_send_messages=False)


def unmute_permissions():
    return types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )


def add_rank(chat_id, user_id, rank_name):
    ranks = load_ranks()
    gid = str(chat_id)
    uid = str(user_id)

    if gid not in ranks:
        ranks[gid] = {"owners": [], "admins_local": [], "vips": []}

    for key in ["owners", "admins_local", "vips"]:
        if uid in ranks[gid][key]:
            ranks[gid][key].remove(uid)

    ranks[gid][rank_name].append(uid)
    save_ranks(ranks)


def remove_rank(chat_id, user_id, rank_name):
    ranks = load_ranks()
    gid = str(chat_id)
    uid = str(user_id)

    if gid in ranks and uid in ranks[gid].get(rank_name, []):
        ranks[gid][rank_name].remove(uid)
        save_ranks(ranks)


def set_lock(chat_id, key, state):
    groups = load_groups()
    gid = str(chat_id)
    groups[gid]["locks"][key] = state
    save_groups(groups)


def notify_owner(text):
    try:
        bot.send_message(OWNER_ID, text)
    except:
        pass


# =========================
# الأزرار
# =========================
def main_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("① اوامر الادمنيه", callback_data="admin_cmds"),
        types.InlineKeyboardButton("② اوامر الرفع والتنزيل", callback_data="rank_cmds"),
        types.InlineKeyboardButton("③ اوامر القفل والفتح", callback_data="lock_cmds"),
        types.InlineKeyboardButton("④ اوامر الاعدادات", callback_data="settings_cmds"),
        types.InlineKeyboardButton("⑤ اوامر التسلية", callback_data="fun_cmds"),
        types.InlineKeyboardButton("⑥ اوامر Dev", callback_data="dev_cmds"),
        types.InlineKeyboardButton("⑦ الاوامر الخدمية", callback_data="service_cmds"),
    )
    return markup


def back_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("رجوع", callback_data="back_main"))
    return markup


# =========================
# /start
# =========================
@bot.message_handler(commands=["start"])
def start_command(message):
    ensure_user(message.from_user)

    username = f"@{message.from_user.username}" if message.from_user.username else "لا يوجد"
    notify_owner(
        "📥 شخص دخل البوت\n\n"
        f"• الاسم: {message.from_user.first_name}\n"
        f"• اليوزر: {username}\n"
        f"• الايدي: <code>{message.from_user.id}</code>"
    )

    if not is_subscribed(message.from_user.id):
        return force_sub(message)

    caption = (
        "🌿 أهلاً بك في بوت الحماية\n"
        "- أرسل كلمة: الاوامر\n"
        "- حتى تظهر لك الأقسام"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("المطور", url=f"https://t.me/{DEV_USERNAME}"),
        types.InlineKeyboardButton("اضفني +", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
    )
    markup.add(types.InlineKeyboardButton("القناة", url=f"https://t.me/{CHANNEL_USERNAME}"))

    try:
        with open("welcome.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=caption, reply_markup=markup)
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup)


# =========================
# قائمة الأوامر
# =========================
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["الاوامر", "اوامر", "/help"])
def show_main_menu(message):
    ensure_user(message.from_user)

    if not is_subscribed(message.from_user.id):
        return force_sub(message)

    text = (
        "• قائمة الأوامر :\n\n"
        "━━━━━━━━━━━━\n"
        "1- أوامر الادمنية\n"
        "2- أوامر الرفع والتنزيل\n"
        "3- أوامر القفل والفتح\n"
        "4- أوامر الإعدادات\n"
        "5- أوامر التسلية\n"
        "6- أوامر Dev\n"
        "7- الأوامر الخدمية\n"
        "━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    sections = {
        "admin_cmds": """• أوامر الادمنيه :

━━━━━━━━━━━━
• كتم
• الغاء كتم
• حظر
• الغاء حظر
• طرد
• تثبيت
• الغاء تثبيت
• حذف
• انذار
• مسح المكتومين
• مسح المحظورين
━━━━━━━━━━━━
• ملاحظة: بالرد على رسالة الشخص""",

        "rank_cmds": """• أوامر الرفع والتنزيل :

━━━━━━━━━━━━
• رفع مالك
• تنزيل مالك
• رفع ادمن
• تنزيل ادمن
• رفع مميز
• تنزيل مميز
━━━━━━━━━━━━""",

        "lock_cmds": """• أوامر القفل والفتح :

━━━━━━━━━━━━
• قفل الروابط
• فتح الروابط
• قفل الصور
• فتح الصور
• قفل الفيديو
• فتح الفيديو
• قفل الملصقات
• فتح الملصقات
• قفل التوجيه
• فتح التوجيه
• قفل البوتات
• فتح البوتات
• قفل الدردشه
• فتح الدردشه
• قفل المعرف
• فتح المعرف
━━━━━━━━━━━━""",

        "settings_cmds": """• أوامر الاعدادات :

━━━━━━━━━━━━
• تفعيل الترحيب
• تعطيل الترحيب
• وضع ترحيب + النص
• حذف الترحيب
• تعيين القوانين + النص
• عرض القوانين
• حذف القوانين
• تعيين وصف + النص
• عرض الوصف
• عرض الاعدادات
━━━━━━━━━━━━""",

        "fun_cmds": """• أوامر التسلية :

━━━━━━━━━━━━
• حقيقة
• تحدي
• حكم
━━━━━━━━━━━━""",

        "dev_cmds": f"""• أوامر Dev :

━━━━━━━━━━━━
• المطور : @{DEV_USERNAME}
• القناة : @{CHANNEL_USERNAME}
━━━━━━━━━━━━""",

        "service_cmds": """• الأوامر الخدمية :

━━━━━━━━━━━━
• الاوامر
• مطور
• ايدي
• معلوماتي
• الرابط
• الوقت
• التاريخ
━━━━━━━━━━━━"""
    }

    try:
        if call.data == "back_main":
            text = (
                "• قائمة الأوامر :\n\n"
                "━━━━━━━━━━━━\n"
                "1- أوامر الادمنية\n"
                "2- أوامر الرفع والتنزيل\n"
                "3- أوامر القفل والفتح\n"
                "4- أوامر الإعدادات\n"
                "5- أوامر التسلية\n"
                "6- أوامر Dev\n"
                "7- الأوامر الخدمية\n"
                "━━━━━━━━━━━━"
            )
            bot.send_message(call.message.chat.id, text, reply_markup=main_menu_markup())

        elif call.data in sections:
            bot.send_message(call.message.chat.id, sections[call.data], reply_markup=back_markup())

        bot.answer_callback_query(call.id)

    except Exception as e:
        print("Callback Error:", e)
        try:
            bot.answer_callback_query(call.id, "صار خطأ، جرب مرة ثانية")
        except:
            pass


# =========================
# أوامر خدمية
# =========================
@bot.message_handler(func=lambda m: m.text == "مطور")
def developer_command(message):
    bot.reply_to(message, f"👨‍💻 المطور:\nhttps://t.me/{DEV_USERNAME}")


@bot.message_handler(func=lambda m: m.text == "ايدي")
def my_id(message):
    bot.reply_to(message, f"🆔 ايديك: <code>{message.from_user.id}</code>")


@bot.message_handler(func=lambda m: m.text == "معلوماتي")
def my_info(message):
    rank = get_local_rank(message.chat.id, message.from_user.id) if is_group(message) else None
    text = (
        f"• الاسم: {message.from_user.first_name}\n"
        f"• الايدي: <code>{message.from_user.id}</code>\n"
        f"• المعرف: @{message.from_user.username if message.from_user.username else 'لا يوجد'}\n"
        f"• الرتبة: {rank if rank else 'عضو'}"
    )
    bot.reply_to(message, text)


@bot.message_handler(func=lambda m: m.text == "الوقت")
def current_time(message):
    bot.reply_to(message, f"🕒 الوقت: {datetime.now().strftime('%H:%M:%S')}")


@bot.message_handler(func=lambda m: m.text == "التاريخ")
def current_date(message):
    bot.reply_to(message, f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d')}")


@bot.message_handler(func=lambda m: m.text == "الرابط")
def group_link(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    try:
        link = bot.export_chat_invite_link(message.chat.id)
        bot.reply_to(message, f"🔗 رابط المجموعة:\n{link}")
    except:
        bot.reply_to(message, "❌ البوت يحتاج صلاحية دعوة عبر الرابط.")


# =========================
# رفع وتنزيل
# =========================
@bot.message_handler(func=lambda m: m.text == "رفع مالك")
def raise_owner(message):
    if not is_group(message):
        return
    if not has_owner_power(message.chat.id, message.from_user.id):
        return owner_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    add_rank(message.chat.id, target.id, "owners")
    bot.reply_to(message, f"✅ تم رفعه مالك\n{mention(target)}")


@bot.message_handler(func=lambda m: m.text == "تنزيل مالك")
def demote_owner(message):
    if not is_group(message):
        return
    if not has_owner_power(message.chat.id, message.from_user.id):
        return owner_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    remove_rank(message.chat.id, target.id, "owners")
    bot.reply_to(message, f"✅ تم تنزيله من مالك\n{mention(target)}")


@bot.message_handler(func=lambda m: m.text == "رفع ادمن")
def raise_admin(message):
    if not is_group(message):
        return
    if not has_owner_power(message.chat.id, message.from_user.id):
        return owner_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    add_rank(message.chat.id, target.id, "admins_local")
    bot.reply_to(message, f"✅ تم رفعه ادمن\n{mention(target)}")


@bot.message_handler(func=lambda m: m.text == "تنزيل ادمن")
def demote_admin(message):
    if not is_group(message):
        return
    if not has_owner_power(message.chat.id, message.from_user.id):
        return owner_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    remove_rank(message.chat.id, target.id, "admins_local")
    bot.reply_to(message, f"✅ تم تنزيله من ادمن\n{mention(target)}")


@bot.message_handler(func=lambda m: m.text == "رفع مميز")
def raise_vip(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    add_rank(message.chat.id, target.id, "vips")
    bot.reply_to(message, f"✅ تم رفعه مميز\n{mention(target)}")


@bot.message_handler(func=lambda m: m.text == "تنزيل مميز")
def demote_vip(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    remove_rank(message.chat.id, target.id, "vips")
    bot.reply_to(message, f"✅ تم تنزيله من مميز\n{mention(target)}")


# =========================
# أوامر الادمنية
# =========================
@bot.message_handler(func=lambda m: m.text == "كتم")
def mute_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")
    if protected_target(message.chat.id, target.id):
        return bot.reply_to(message, "❌ ما اكدر أكتم هذا الشخص.")

    try:
        bot.restrict_chat_member(message.chat.id, target.id, permissions=mute_permissions())
        groups = load_groups()
        gid = str(message.chat.id)
        if str(target.id) not in groups[gid]["muted"]:
            groups[gid]["muted"].append(str(target.id))
            save_groups(groups)
        bot.reply_to(message, f"🔇 تم كتم {mention(target)}")
    except:
        bot.reply_to(message, "❌ فشل الكتم. تأكد البوت أدمن وعنده صلاحية تقييد.")


@bot.message_handler(func=lambda m: m.text in ["الغاء كتم", "إلغاء كتم", "فك كتم"])
def unmute_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    try:
        bot.restrict_chat_member(message.chat.id, target.id, permissions=unmute_permissions())
        groups = load_groups()
        gid = str(message.chat.id)
        if str(target.id) in groups[gid]["muted"]:
            groups[gid]["muted"].remove(str(target.id))
            save_groups(groups)
        bot.reply_to(message, f"🔊 تم الغاء كتم {mention(target)}")
    except:
        bot.reply_to(message, "❌ فشل الغاء الكتم.")


@bot.message_handler(func=lambda m: m.text == "حظر")
def ban_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")
    if protected_target(message.chat.id, target.id):
        return bot.reply_to(message, "❌ ما اكدر أحظر هذا الشخص.")

    try:
        bot.ban_chat_member(message.chat.id, target.id)
        groups = load_groups()
        gid = str(message.chat.id)
        if str(target.id) not in groups[gid]["banned"]:
            groups[gid]["banned"].append(str(target.id))
            save_groups(groups)
        bot.reply_to(message, f"🚫 تم حظر {mention(target)}")
    except:
        bot.reply_to(message, "❌ فشل الحظر.")


@bot.message_handler(func=lambda m: m.text in ["الغاء حظر", "إلغاء حظر", "فك حظر"])
def unban_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص أو تكتب ايديه.")

    try:
        bot.unban_chat_member(message.chat.id, target.id, only_if_banned=False)
        groups = load_groups()
        gid = str(message.chat.id)
        if str(target.id) in groups[gid]["banned"]:
            groups[gid]["banned"].remove(str(target.id))
            save_groups(groups)
        bot.reply_to(message, f"✅ تم الغاء حظر {mention(target)}")
    except:
        bot.reply_to(message, "❌ فشل الغاء الحظر.")


@bot.message_handler(func=lambda m: m.text == "طرد")
def kick_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")
    if protected_target(message.chat.id, target.id):
        return bot.reply_to(message, "❌ ما اكدر أطرد هذا الشخص.")

    try:
        bot.ban_chat_member(message.chat.id, target.id)
        bot.unban_chat_member(message.chat.id, target.id)
        bot.reply_to(message, f"👢 تم طرد {mention(target)}")
    except:
        bot.reply_to(message, "❌ فشل الطرد.")


@bot.message_handler(func=lambda m: m.text == "حذف")
def delete_replied(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)
    if not message.reply_to_message:
        return bot.reply_to(message, "❌ لازم ترد على رسالة.")

    try:
        bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        bot.delete_message(message.chat.id, message.message_id)
    except:
        bot.reply_to(message, "❌ ما كدرت أحذف الرسالة.")


@bot.message_handler(func=lambda m: m.text == "تثبيت")
def pin_message(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)
    if not message.reply_to_message:
        return bot.reply_to(message, "❌ لازم ترد على رسالة.")

    try:
        bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        bot.reply_to(message, "📌 تم تثبيت الرسالة.")
    except:
        bot.reply_to(message, "❌ فشل التثبيت.")


@bot.message_handler(func=lambda m: m.text == "الغاء تثبيت")
def unpin_messages(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    try:
        bot.unpin_all_chat_messages(message.chat.id)
        bot.reply_to(message, "✅ تم الغاء التثبيت.")
    except:
        bot.reply_to(message, "❌ فشل الغاء التثبيت.")


@bot.message_handler(func=lambda m: m.text == "انذار")
def warn_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)
    if not message.reply_to_message:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    target = message.reply_to_message.from_user
    if protected_target(message.chat.id, target.id):
        return bot.reply_to(message, "❌ ما اكدر أنذر هذا الشخص.")

    groups = load_groups()
    gid = str(message.chat.id)
    uid = str(target.id)

    warns = groups[gid]["warns"]
    warns[uid] = warns.get(uid, 0) + 1
    count = warns[uid]
    save_groups(groups)

    if count >= 3:
        try:
            bot.ban_chat_member(message.chat.id, target.id)
            if uid not in groups[gid]["banned"]:
                groups[gid]["banned"].append(uid)
                save_groups(groups)
            bot.reply_to(message, f"🚫 تم حظر {mention(target)} بعد 3 إنذارات.")
        except:
            bot.reply_to(message, f"⚠️ انذار رقم {count} لـ {mention(target)}")
    else:
        bot.reply_to(message, f"⚠️ انذار رقم {count} لـ {mention(target)}")


@bot.message_handler(func=lambda m: m.text == "مسح المكتومين")
def clear_muted(message):
    if not is_group(message):
        return
    if not has_owner_power(message.chat.id, message.from_user.id):
        return owner_only(message)

    groups = load_groups()
    gid = str(message.chat.id)

    for uid in groups[gid]["muted"][:]:
        try:
            bot.restrict_chat_member(message.chat.id, int(uid), permissions=unmute_permissions())
        except:
            pass

    groups[gid]["muted"] = []
    save_groups(groups)
    bot.reply_to(message, "✅ تم مسح المكتومين.")


@bot.message_handler(func=lambda m: m.text == "مسح المحظورين")
def clear_banned(message):
    if not is_group(message):
        return
    if not has_owner_power(message.chat.id, message.from_user.id):
        return owner_only(message)

    groups = load_groups()
    gid = str(message.chat.id)

    for uid in groups[gid]["banned"][:]:
        try:
            bot.unban_chat_member(message.chat.id, int(uid), only_if_banned=False)
        except:
            pass

    groups[gid]["banned"] = []
    save_groups(groups)
    bot.reply_to(message, "✅ تم مسح المحظورين.")


# =========================
# قفل وفتح
# =========================
@bot.message_handler(func=lambda m: m.text and m.text.startswith("قفل "))
def lock_command(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = message.text.replace("قفل ", "", 1).strip()
    mapping = {
        "الروابط": "links",
        "الصور": "photos",
        "الفيديو": "videos",
        "الملصقات": "stickers",
        "التوجيه": "forwards",
        "البوتات": "bots",
        "الدردشه": "chat",
        "الدردشة": "chat",
        "المعرف": "usernames",
    }

    if target not in mapping:
        return bot.reply_to(message, "❌ هذا النوع غير مدعوم.")

    set_lock(message.chat.id, mapping[target], True)
    bot.reply_to(message, f"✅ تم قفل {target}")


@bot.message_handler(func=lambda m: m.text and m.text.startswith("فتح "))
def unlock_command(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = message.text.replace("فتح ", "", 1).strip()
    mapping = {
        "الروابط": "links",
        "الصور": "photos",
        "الفيديو": "videos",
        "الملصقات": "stickers",
        "التوجيه": "forwards",
        "البوتات": "bots",
        "الدردشه": "chat",
        "الدردشة": "chat",
        "المعرف": "usernames",
    }

    if target not in mapping:
        return bot.reply_to(message, "❌ هذا النوع غير مدعوم.")

    set_lock(message.chat.id, mapping[target], False)
    bot.reply_to(message, f"✅ تم فتح {target}")


# =========================
# الإعدادات
# =========================
@bot.message_handler(func=lambda m: m.text == "تفعيل الترحيب")
def enable_welcome(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    groups = load_groups()
    groups[str(message.chat.id)]["welcome_enabled"] = True
    save_groups(groups)
    bot.reply_to(message, "✅ تم تفعيل الترحيب.")


@bot.message_handler(func=lambda m: m.text == "تعطيل الترحيب")
def disable_welcome(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    groups = load_groups()
    groups[str(message.chat.id)]["welcome_enabled"] = False
    save_groups(groups)
    bot.reply_to(message, "✅ تم تعطيل الترحيب.")


@bot.message_handler(func=lambda m: m.text and m.text.startswith("وضع ترحيب "))
def set_welcome_text(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    text = message.text.replace("وضع ترحيب ", "", 1).strip()
    if not text:
        return bot.reply_to(message, "❌ اكتب النص بعد الأمر.")

    groups = load_groups()
    groups[str(message.chat.id)]["welcome_text"] = text
    save_groups(groups)
    bot.reply_to(message, "✅ تم حفظ الترحيب.")


@bot.message_handler(func=lambda m: m.text == "حذف الترحيب")
def delete_welcome_text(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    groups = load_groups()
    groups[str(message.chat.id)]["welcome_text"] = "اهلاً {name} نورت {group} 🌿"
    save_groups(groups)
    bot.reply_to(message, "✅ تم حذف الترحيب المخصص.")


@bot.message_handler(func=lambda m: m.text and m.text.startswith("تعيين القوانين "))
def set_rules(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    text = message.text.replace("تعيين القوانين ", "", 1).strip()
    groups = load_groups()
    groups[str(message.chat.id)]["rules"] = text
    save_groups(groups)
    bot.reply_to(message, "✅ تم حفظ القوانين.")


@bot.message_handler(func=lambda m: m.text == "عرض القوانين")
def show_rules(message):
    if not is_group(message):
        return

    data = get_group_data(message.chat.id)
    if not data["rules"]:
        return bot.reply_to(message, "❌ لا توجد قوانين.")
    bot.reply_to(message, f"📜 القوانين:\n{data['rules']}")


@bot.message_handler(func=lambda m: m.text == "حذف القوانين")
def delete_rules(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    groups = load_groups()
    groups[str(message.chat.id)]["rules"] = ""
    save_groups(groups)
    bot.reply_to(message, "✅ تم حذف القوانين.")


@bot.message_handler(func=lambda m: m.text and m.text.startswith("تعيين وصف "))
def set_description(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    text = message.text.replace("تعيين وصف ", "", 1).strip()
    groups = load_groups()
    groups[str(message.chat.id)]["description"] = text
    save_groups(groups)
    bot.reply_to(message, "✅ تم حفظ الوصف.")


@bot.message_handler(func=lambda m: m.text == "عرض الوصف")
def show_description(message):
    if not is_group(message):
        return

    data = get_group_data(message.chat.id)
    if not data["description"]:
        return bot.reply_to(message, "❌ لا يوجد وصف.")
    bot.reply_to(message, f"📝 الوصف:\n{data['description']}")


@bot.message_handler(func=lambda m: m.text == "عرض الاعدادات")
def show_settings(message):
    if not is_group(message):
        return

    data = get_group_data(message.chat.id)
    locks = data["locks"]

    text = (
        f"• الترحيب: {'مفعل' if data['welcome_enabled'] else 'معطل'}\n"
        f"• الروابط: {'مقفول' if locks['links'] else 'مفتوح'}\n"
        f"• الصور: {'مقفول' if locks['photos'] else 'مفتوح'}\n"
        f"• الفيديو: {'مقفول' if locks['videos'] else 'مفتوح'}\n"
        f"• الملصقات: {'مقفول' if locks['stickers'] else 'مفتوح'}\n"
        f"• التوجيه: {'مقفول' if locks['forwards'] else 'مفتوح'}\n"
        f"• البوتات: {'مقفول' if locks['bots'] else 'مفتوح'}\n"
        f"• الدردشة: {'مقفول' if locks['chat'] else 'مفتوح'}\n"
        f"• المعرف: {'مقفول' if locks['usernames'] else 'مفتوح'}"
    )
    bot.reply_to(message, text)


# =========================
# دخول أعضاء جدد
# =========================
@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_members(message):
    if not is_group(message):
        return

    ensure_group(message.chat)
    data = get_group_data(message.chat.id)

    for member in message.new_chat_members:
        username = f"@{member.username}" if member.username else "لا يوجد"
        inviter_name = message.from_user.first_name if message.from_user else "غير معروف"
        inviter_id = message.from_user.id if message.from_user else "غير معروف"

        notify_owner(
            "🚨 عضو جديد دخل الكروب\n\n"
            f"• الاسم: {member.first_name}\n"
            f"• اليوزر: {username}\n"
            f"• الايدي: <code>{member.id}</code>\n"
            f"• اسم الكروب: {message.chat.title}\n"
            f"• ايدي الكروب: <code>{message.chat.id}</code>\n"
            f"• الشخص الظاهر بالحدث: {inviter_name}\n"
            f"• ايديه: <code>{inviter_id}</code>"
        )

        if data["locks"]["bots"] and member.is_bot:
            try:
                bot.ban_chat_member(message.chat.id, member.id)
            except:
                pass

    if not data["welcome_enabled"]:
        return

    for member in message.new_chat_members:
        text = data["welcome_text"]
        text = text.replace("{name}", member.first_name or "عضو")
        text = text.replace("{group}", message.chat.title or "المجموعة")
        try:
            with open("welcome.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption=text)
        except:
            bot.send_message(message.chat.id, text)


# =========================
# حماية تلقائية
# =========================
@bot.message_handler(content_types=["text", "photo", "video", "sticker", "document", "audio", "voice"])
def auto_protection(message):
    ensure_user(message.from_user)
    if is_group(message):
        ensure_group(message.chat)

    if not is_group(message):
        return

    groups = load_groups()
    gid = str(message.chat.id)

    if str(message.from_user.id) in groups[gid]["muted"]:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        return

    if has_admin_power(message.chat.id, message.from_user.id):
        return

    data = get_group_data(message.chat.id)
    locks = data["locks"]

    try:
        if message.content_type == "text":
            txt = message.text or ""

            if locks["chat"]:
                bot.delete_message(message.chat.id, message.message_id)
                return

            if locks["links"] and re.search(r"(https?://|t\.me/|www\.)", txt, re.IGNORECASE):
                bot.delete_message(message.chat.id, message.message_id)
                return

            if locks["usernames"] and "@" in txt:
                bot.delete_message(message.chat.id, message.message_id)
                return

            if (getattr(message, "forward_from", None) or getattr(message, "forward_from_chat", None)) and locks["forwards"]:
                bot.delete_message(message.chat.id, message.message_id)
                return

        if message.content_type == "photo" and locks["photos"]:
            bot.delete_message(message.chat.id, message.message_id)
            return

        if message.content_type == "video" and locks["videos"]:
            bot.delete_message(message.chat.id, message.message_id)
            return

        if message.content_type == "sticker" and locks["stickers"]:
            bot.delete_message(message.chat.id, message.message_id)
            return

    except:
        pass


print("Bot is running...")
bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
