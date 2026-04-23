import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
import json
import os
import re
from datetime import datetime

BOT_TOKEN = "8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74"
BOT_USERNAME = "@Fadifvbot"
DEV_USERNAME = "fvamv"
DEV_ID = 8065884629  # حط ايديك الرقمي هنا

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# =========================
# ملفات الداتا
# =========================
if not os.path.exists("data"):
    os.makedirs("data")

DATA_FILES = {
    "users": "data/users.json",
    "groups": "data/groups.json",
    "ranks": "data/ranks.json",
    "settings": "data/settings.json"
}

for path in DATA_FILES.values():
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)


def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_users():
    return load_data(DATA_FILES["users"])


def save_users(data):
    save_data(DATA_FILES["users"], data)


def load_groups():
    return load_data(DATA_FILES["groups"])


def save_groups(data):
    save_data(DATA_FILES["groups"], data)


def load_ranks():
    return load_data(DATA_FILES["ranks"])


def save_ranks(data):
    save_data(DATA_FILES["ranks"], data)


def load_settings():
    return load_data(DATA_FILES["settings"])


def save_settings(data):
    save_data(DATA_FILES["settings"], data)


# =========================
# تهيئة البيانات
# =========================
DEFAULT_LOCKS = {
    "links": False,
    "username": False,
    "tag": False,
    "edit": False,
    "gif": False,
    "photos": False,
    "video": False,
    "voice": False,
    "audio": False,
    "files": False,
    "stickers": False,
    "forward": False,
    "bots": False,
    "chat": False,
}

DEFAULT_GROUP_SETTINGS = {
    "welcome_enabled": False,
    "welcome_text": "أهلاً بك {name} في {group}",
    "rules": "",
    "description": "",
    "warns": {},
    "locks": DEFAULT_LOCKS.copy(),
    "mutes": [],
    "bans": []
}


def ensure_user(user):
    users = load_users()
    uid = str(user.id)
    if uid not in users:
        users[uid] = {
            "name": user.first_name or "",
            "username": user.username or "",
        }
        save_users(users)


def ensure_group(chat):
    groups = load_groups()
    gid = str(chat.id)
    if gid not in groups:
        groups[gid] = DEFAULT_GROUP_SETTINGS.copy()
        groups[gid]["locks"] = DEFAULT_LOCKS.copy()
        save_groups(groups)

    ranks = load_ranks()
    if gid not in ranks:
        ranks[gid] = {
            "owner_basic": [],
            "owners": [],
            "supervisors": [],
            "admins_local": [],
            "vips": []
        }
        save_ranks(ranks)


# =========================
# أدوات مساعدة
# =========================
def is_group(message):
    return message.chat.type in ["group", "supergroup"]


def is_dev(user_id):
    return int(user_id) == int(DEV_ID)


def get_group_rank(chat_id, user_id):
    ranks = load_ranks()
    gid = str(chat_id)
    uid = str(user_id)

    if gid not in ranks:
        return None

    if uid in ranks[gid].get("owner_basic", []):
        return "owner_basic"
    if uid in ranks[gid].get("owners", []):
        return "owner"
    if uid in ranks[gid].get("supervisors", []):
        return "supervisor"
    if uid in ranks[gid].get("admins_local", []):
        return "admin_local"
    if uid in ranks[gid].get("vips", []):
        return "vip"
    return None


def is_telegram_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False


def has_admin_power(chat_id, user_id):
    if is_dev(user_id):
        return True
    if is_telegram_admin(chat_id, user_id):
        return True
    rank = get_group_rank(chat_id, user_id)
    return rank in ["owner_basic", "owner", "supervisor", "admin_local"]


def has_high_rank(chat_id, user_id):
    if is_dev(user_id):
        return True
    if is_telegram_admin(chat_id, user_id):
        return True
    rank = get_group_rank(chat_id, user_id)
    return rank in ["owner_basic", "owner", "supervisor"]


def has_owner_rank(chat_id, user_id):
    if is_dev(user_id):
        return True
    if is_telegram_admin(chat_id, user_id):
        return True
    rank = get_group_rank(chat_id, user_id)
    return rank in ["owner_basic", "owner"]


def admin_only(message):
    bot.reply_to(message, "❌ هذا الأمر فقط للمشرف وفوك.")


def high_only(message):
    bot.reply_to(message, "❌ هذا الأمر فقط للمالك أو المشرف الأعلى.")


def owner_only(message):
    bot.reply_to(message, "❌ هذا الأمر فقط للمالك.")


def get_target_user(message):
    if message.reply_to_message:
        return message.reply_to_message.from_user

    parts = (message.text or "").split()
    if len(parts) >= 2 and parts[1].isdigit():
        class TempUser:
            def __init__(self, uid):
                self.id = int(uid)
                self.first_name = uid
        return TempUser(parts[1])

    return None


def target_is_protected(chat_id, user_id):
    if is_dev(user_id):
        return True
    if is_telegram_admin(chat_id, user_id):
        return True
    rank = get_group_rank(chat_id, user_id)
    return rank in ["owner_basic", "owner", "supervisor", "admin_local"]


def mute_permissions():
    return types.ChatPermissions(
        can_send_messages=False
    )


def unmute_permissions():
    return types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )


def mention_user(user):
    name = user.first_name if hasattr(user, "first_name") else str(user.id)
    return f"<a href='tg://user?id={user.id}'>{name}</a>"


def add_rank(chat_id, user_id, rank_name):
    ranks = load_ranks()
    gid = str(chat_id)
    uid = str(user_id)
    ensure_group(bot.get_chat(chat_id))

    for key in ["owner_basic", "owners", "supervisors", "admins_local", "vips"]:
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


def clear_rank(chat_id, rank_name):
    ranks = load_ranks()
    gid = str(chat_id)
    if gid in ranks:
        ranks[gid][rank_name] = []
        save_ranks(ranks)


def lock_name_map(ar_name):
    mapping = {
        "الروابط": "links",
        "المعرف": "username",
        "التاك": "tag",
        "التعديل": "edit",
        "المتحركة": "gif",
        "الصور": "photos",
        "الفيديو": "video",
        "الصوت": "voice",
        "الصوتيات": "audio",
        "الملفات": "files",
        "الملصقات": "stickers",
        "التوجيه": "forward",
        "البوتات": "bots",
        "الدردشه": "chat",
        "الدردشة": "chat",
    }
    return mapping.get(ar_name)


def set_lock(chat_id, lock_key, value):
    groups = load_groups()
    gid = str(chat_id)
    ensure_group(bot.get_chat(chat_id))
    groups = load_groups()
    groups[gid]["locks"][lock_key] = value
    save_groups(groups)


def get_group_data(chat_id):
    ensure_group(bot.get_chat(chat_id))
    groups = load_groups()
    return groups[str(chat_id)]


# =========================
# تسجيل المستخدمين والكروبات
# =========================
@bot.message_handler(func=lambda m: True, content_types=[
    'text', 'photo', 'video', 'audio', 'voice', 'document', 'sticker',
    'animation', 'new_chat_members', 'left_chat_member'
])
def global_handler(message):
    ensure_user(message.from_user)
    if message.chat.type in ["group", "supergroup"]:
        ensure_group(message.chat)

    process_auto_actions(message)
    process_commands(message)


# =========================
# الحماية التلقائية
# =========================
def process_auto_actions(message):
    if not is_group(message):
        return

    if has_admin_power(message.chat.id, message.from_user.id):
        return

    data = get_group_data(message.chat.id)
    locks = data["locks"]

    if locks["chat"] and message.content_type == "text":
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        return

    if locks["photos"] and message.content_type == "photo":
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    if locks["video"] and message.content_type == "video":
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    if locks["voice"] and message.content_type == "voice":
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    if locks["audio"] and message.content_type == "audio":
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    if locks["files"] and message.content_type == "document":
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    if locks["stickers"] and message.content_type == "sticker":
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    if locks["gif"] and message.content_type == "animation":
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    if locks["forward"] and getattr(message, "forward_from", None):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    if locks["bots"] and message.content_type == "new_chat_members":
        try:
            for member in message.new_chat_members:
                if member.is_bot:
                    bot.ban_chat_member(message.chat.id, member.id)
        except:
            pass

    if locks["edit"] and getattr(message, "edit_date", None):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    if message.content_type == "text":
        text = message.text or ""

        if locks["links"] and re.search(r"(https?://|t\.me/|www\.)", text, re.IGNORECASE):
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            return

        if locks["username"] and "@" in text:
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            return

        if locks["tag"] and "#" in text:
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            return


# =========================
# معالجة الأوامر
# =========================
def process_commands(message):
    if message.content_type != "text":
        if message.content_type == "new_chat_members":
            handle_welcome(message)
        return

    text = (message.text or "").strip()

    if text == "/start":
        return start_command(message)
    if text == "مطور":
        return developer_command(message)
    if text in ["الاوامر", "اوامر", "/help", "اوامر البوت"]:
        return show_main_menu(message)

    if text == "ايدي":
        return bot.reply_to(message, f"🆔 ايديك: <code>{message.from_user.id}</code>")
    if text == "معلوماتي":
        rank = get_group_rank(message.chat.id, message.from_user.id) if is_group(message) else None
        txt = (
            f"• الاسم: {message.from_user.first_name}\n"
            f"• الايدي: <code>{message.from_user.id}</code>\n"
            f"• المعرف: @{message.from_user.username if message.from_user.username else 'لا يوجد'}\n"
            f"• رتبتك: {rank if rank else 'عضو'}"
        )
        return bot.reply_to(message, txt)

    if text == "الوقت":
        return bot.reply_to(message, f"🕒 الوقت: {datetime.now().strftime('%H:%M:%S')}")
    if text == "التاريخ":
        return bot.reply_to(message, f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d')}")

    if text == "الرابط":
        if not is_group(message):
            return
        if not has_admin_power(message.chat.id, message.from_user.id):
            return admin_only(message)
        try:
            link = bot.export_chat_invite_link(message.chat.id)
            return bot.reply_to(message, f"🔗 رابط المجموعة:\n{link}")
        except:
            return bot.reply_to(message, "❌ ما كدرت أجيب الرابط. تأكد البوت عنده صلاحية دعوة.")

    # رفع وتنزيل
    if text == "رفع مالك اساسي":
        return rank_command(message, "owner_basic", "تم رفعه مالك اساسي", need="dev")
    if text == "تنزيل مالك اساسي":
        return derank_command(message, "owner_basic", "تم تنزيله من مالك اساسي", need="dev")

    if text == "رفع مالك":
        return rank_command(message, "owners", "تم رفعه مالك", need="owner")
    if text == "تنزيل مالك":
        return derank_command(message, "owners", "تم تنزيله من مالك", need="owner")

    if text == "رفع مشرف":
        return rank_command(message, "supervisors", "تم رفعه مشرف", need="owner")
    if text == "تنزيل مشرف":
        return derank_command(message, "supervisors", "تم تنزيله من مشرف", need="owner")

    if text == "رفع ادمن":
        return rank_command(message, "admins_local", "تم رفعه ادمن", need="high")
    if text == "تنزيل ادمن":
        return derank_command(message, "admins_local", "تم تنزيله من ادمن", need="high")

    if text == "رفع مميز":
        return rank_command(message, "vips", "تم رفعه مميز", need="high")
    if text == "تنزيل مميز":
        return derank_command(message, "vips", "تم تنزيله من مميز", need="high")

    if text == "تنزيل الكل":
        return clear_all_ranks(message)

    # ادمنية
    if text == "كتم":
        return mute_user(message)
    if text in ["الغاء كتم", "إلغاء كتم", "فك كتم"]:
        return unmute_user(message)
    if text == "حظر":
        return ban_user(message)
    if text in ["الغاء حظر", "إلغاء حظر", "فك حظر"]:
        return unban_user(message)
    if text == "طرد":
        return kick_user(message)
    if text == "حذف":
        return delete_replied_message(message)
    if text == "تثبيت":
        return pin_message(message)
    if text == "الغاء تثبيت":
        return unpin_message(message)
    if text == "انذار":
        return warn_user(message)

    # مسح
    if text == "مسح المميزين":
        return clear_specific_rank(message, "vips", "تم مسح المميزين")
    if text == "مسح الادمنية":
        return clear_specific_rank(message, "admins_local", "تم مسح الادمنية")
    if text == "مسح المشرفين":
        return clear_specific_rank(message, "supervisors", "تم مسح المشرفين")
    if text == "مسح المالكين":
        return clear_specific_rank(message, "owners", "تم مسح المالكين")
    if text == "مسح المحظورين":
        return clear_bans(message)
    if text == "مسح المكتومين":
        return clear_mutes(message)

    # قفل / فتح
    if text.startswith("قفل "):
        return lock_command(message, True)
    if text.startswith("فتح "):
        return lock_command(message, False)

    # إعدادات
    if text == "تفعيل الترحيب":
        return toggle_welcome(message, True)
    if text == "تعطيل الترحيب":
        return toggle_welcome(message, False)
    if text.startswith("وضع ترحيب "):
        return set_welcome(message)
    if text == "حذف الترحيب":
        return delete_welcome(message)
    if text.startswith("تعيين القوانين "):
        return set_rules(message)
    if text == "حذف القوانين":
        return delete_rules(message)
    if text == "عرض القوانين":
        return show_rules(message)
    if text.startswith("تعيين وصف "):
        return set_description(message)
    if text == "عرض الوصف":
        return show_description(message)
    if text == "عرض الاعدادات":
        return show_settings(message)

    # Dev
    if text == "عدد المستخدمين":
        return count_users(message)
    if text == "عدد الكروبات":
        return count_groups(message)
    if text.startswith("اذاعة "):
        return broadcast_message(message)

    # ترحيب
    if message.content_type == "new_chat_members":
        return handle_welcome(message)


# =========================
# ستارت ومطور
# =========================
def start_command(message):
    ensure_user(message.from_user)
    caption = (
        "🌿 أهلاً بك في بوت الحماية.\n"
        "- أرسل كلمة: الاوامر\n"
        "- حتى تظهر لك كل الأقسام."
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("المطور", url=f"https://t.me/{DEV_USERNAME}"),
        types.InlineKeyboardButton("اضفني +", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
    )
    markup.add(types.InlineKeyboardButton("شراء بوت مشابه", url=f"https://t.me/{DEV_USERNAME}"))

    try:
        with open("welcome.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=caption, reply_markup=markup)
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup)


def developer_command(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("حساب المطور", url=f"https://t.me/{DEV_USERNAME}"))
    bot.reply_to(message, f"👨‍💻 المطور:\nhttps://t.me/{DEV_USERNAME}", reply_markup=markup)


# =========================
# القوائم
# =========================
def main_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("① اوامر الادمنيه", callback_data="admin_cmds"),
        types.InlineKeyboardButton("② اوامر الرفع والتنزيل", callback_data="rank_cmds"),
        types.InlineKeyboardButton("③ اوامر المسح", callback_data="clean_cmds"),
        types.InlineKeyboardButton("④ اوامر القفل والفتح", callback_data="lock_cmds"),
        types.InlineKeyboardButton("⑤ اوامر الاعدادات", callback_data="settings_cmds"),
        types.InlineKeyboardButton("⑥ اوامر التسلية", callback_data="fun_cmds"),
        types.InlineKeyboardButton("⑦ اوامر Dev", callback_data="dev_cmds"),
        types.InlineKeyboardButton("⑧ الاوامر الخدميه", callback_data="service_cmds"),
    )
    return markup


def back_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("رجوع", callback_data="back_main"))
    return markup


def show_main_menu(message):
    text = (
        "• أهلاً بك عزيزي في قائمة الأوامر :\n\n"
        "━━━━━━━━━━━━\n"
        "1- أوامر الادمنية\n"
        "2- أوامر الرفع والتنزيل\n"
        "3- أوامر المسح\n"
        "4- أوامر القفل والفتح\n"
        "5- أوامر الإعدادات\n"
        "6- أوامر التسلية\n"
        "7- أوامر Dev\n"
        "8- الأوامر الخدمية\n"
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
━━━━━━━━━━━━
• ملاحظة: بالرد على رسالة الشخص""",

        "rank_cmds": """• أوامر الرفع والتنزيل :

━━━━━━━━━━━━
• رفع مالك اساسي
• تنزيل مالك اساسي
• رفع مالك
• تنزيل مالك
• رفع مشرف
• تنزيل مشرف
• رفع ادمن
• تنزيل ادمن
• رفع مميز
• تنزيل مميز
• تنزيل الكل
━━━━━━━━━━━━""",

        "clean_cmds": """• أوامر المسح :

━━━━━━━━━━━━
• مسح المميزين
• مسح الادمنية
• مسح المشرفين
• مسح المالكين
• مسح المحظورين
• مسح المكتومين
━━━━━━━━━━━━""",

        "lock_cmds": """• أوامر القفل - الفتح :

━━━━━━━━━━━━
• قفل - فتح الروابط
• قفل - فتح المعرف
• قفل - فتح التاك
• قفل - فتح التعديل
• قفل - فتح المتحركة
• قفل - فتح الصور
• قفل - فتح الفيديو
• قفل - فتح الصوت
• قفل - فتح الصوتيات
• قفل - فتح الملفات
• قفل - فتح الملصقات
• قفل - فتح الدردشه
• قفل - فتح التوجيه
• قفل - فتح البوتات
━━━━━━━━━━━━""",

        "settings_cmds": """• أوامر الاعدادات :

━━━━━━━━━━━━
• تفعيل الترحيب
• تعطيل الترحيب
• وضع ترحيب + النص
• حذف الترحيب
• تعيين القوانين + النص
• حذف القوانين
• عرض القوانين
• تعيين وصف + النص
• عرض الوصف
• عرض الاعدادات
━━━━━━━━━━━━""",

        "fun_cmds": """• أوامر التسلية :

━━━━━━━━━━━━
• لعبة اكس او
• تحدي
• حقيقة
• حكم
━━━━━━━━━━━━
• هذا القسم واجهة حالياً""",

        "dev_cmds": """• أوامر Dev :

━━━━━━━━━━━━
• اذاعة + النص
• عدد المستخدمين
• عدد الكروبات
━━━━━━━━━━━━""",

        "service_cmds": """• الأوامر الخدمية :

━━━━━━━━━━━━
• الاوامر
• مطور
• /start
• ايدي
• معلوماتي
• الرابط
• الوقت
• التاريخ
━━━━━━━━━━━━"""
    }

    if call.data == "back_main":
        text = (
            "• أهلاً بك عزيزي في قائمة الأوامر :\n\n"
            "━━━━━━━━━━━━\n"
            "1- أوامر الادمنية\n"
            "2- أوامر الرفع والتنزيل\n"
            "3- أوامر المسح\n"
            "4- أوامر القفل والفتح\n"
            "5- أوامر الإعدادات\n"
            "6- أوامر التسلية\n"
            "7- أوامر Dev\n"
            "8- الأوامر الخدمية\n"
            "━━━━━━━━━━━━"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=main_menu_markup())
    elif call.data in sections:
        bot.edit_message_text(sections[call.data], call.message.chat.id, call.message.message_id, reply_markup=back_markup())

    bot.answer_callback_query(call.id)


# =========================
# رفع وتنزيل
# =========================
def rank_command(message, rank_name, success_text, need="high"):
    if not is_group(message):
        return
    if need == "dev" and not is_dev(message.from_user.id):
        return bot.reply_to(message, "❌ هذا الأمر فقط للمطور.")
    if need == "owner" and not has_owner_rank(message.chat.id, message.from_user.id):
        return owner_only(message)
    if need == "high" and not has_high_rank(message.chat.id, message.from_user.id):
        return high_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    add_rank(message.chat.id, target.id, rank_name)
    bot.reply_to(message, f"✅ {success_text}\n{mention_user(target)}")


def derank_command(message, rank_name, success_text, need="high"):
    if not is_group(message):
        return
    if need == "dev" and not is_dev(message.from_user.id):
        return bot.reply_to(message, "❌ هذا الأمر فقط للمطور.")
    if need == "owner" and not has_owner_rank(message.chat.id, message.from_user.id):
        return owner_only(message)
    if need == "high" and not has_high_rank(message.chat.id, message.from_user.id):
        return high_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    remove_rank(message.chat.id, target.id, rank_name)
    bot.reply_to(message, f"✅ {success_text}\n{mention_user(target)}")


def clear_all_ranks(message):
    if not is_group(message):
        return
    if not has_owner_rank(message.chat.id, message.from_user.id):
        return owner_only(message)

    ranks = load_ranks()
    gid = str(message.chat.id)
    if gid in ranks:
        ranks[gid]["owners"] = []
        ranks[gid]["supervisors"] = []
        ranks[gid]["admins_local"] = []
        ranks[gid]["vips"] = []
        save_ranks(ranks)
    bot.reply_to(message, "✅ تم تنزيل الكل.")


# =========================
# الادمنية
# =========================
def mute_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")
    if target_is_protected(message.chat.id, target.id):
        return bot.reply_to(message, "❌ ما أگدر أكتم هذا الشخص.")

    try:
        bot.restrict_chat_member(message.chat.id, target.id, permissions=mute_permissions())
        groups = load_groups()
        gid = str(message.chat.id)
        if str(target.id) not in groups[gid]["mutes"]:
            groups[gid]["mutes"].append(str(target.id))
            save_groups(groups)
        bot.reply_to(message, f"🔇 تم كتم {mention_user(target)}")
    except:
        bot.reply_to(message, "❌ فشل الكتم.")


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
        if str(target.id) in groups[gid]["mutes"]:
            groups[gid]["mutes"].remove(str(target.id))
            save_groups(groups)
        bot.reply_to(message, f"🔊 تم الغاء كتم {mention_user(target)}")
    except:
        bot.reply_to(message, "❌ فشل الغاء الكتم.")


def ban_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")
    if target_is_protected(message.chat.id, target.id):
        return bot.reply_to(message, "❌ ما أگدر أحظر هذا الشخص.")

    try:
        bot.ban_chat_member(message.chat.id, target.id)
        groups = load_groups()
        gid = str(message.chat.id)
        if str(target.id) not in groups[gid]["bans"]:
            groups[gid]["bans"].append(str(target.id))
            save_groups(groups)
        bot.reply_to(message, f"🚫 تم حظر {mention_user(target)}")
    except:
        bot.reply_to(message, "❌ فشل الحظر.")


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
        if str(target.id) in groups[gid]["bans"]:
            groups[gid]["bans"].remove(str(target.id))
            save_groups(groups)
        bot.reply_to(message, f"✅ تم الغاء حظر {mention_user(target)}")
    except:
        bot.reply_to(message, "❌ فشل الغاء الحظر.")


def kick_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)

    target = get_target_user(message)
    if not target:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")
    if target_is_protected(message.chat.id, target.id):
        return bot.reply_to(message, "❌ ما أگدر أطرد هذا الشخص.")

    try:
        bot.ban_chat_member(message.chat.id, target.id)
        bot.unban_chat_member(message.chat.id, target.id)
        bot.reply_to(message, f"👢 تم طرد {mention_user(target)}")
    except:
        bot.reply_to(message, "❌ فشل الطرد.")


def delete_replied_message(message):
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


def unpin_message(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)
    try:
        bot.unpin_all_chat_messages(message.chat.id)
        bot.reply_to(message, "✅ تم الغاء التثبيت.")
    except:
        bot.reply_to(message, "❌ فشل الغاء التثبيت.")


def warn_user(message):
    if not is_group(message):
        return
    if not has_admin_power(message.chat.id, message.from_user.id):
        return admin_only(message)
    if not message.reply_to_message:
        return bot.reply_to(message, "❌ لازم ترد على رسالة الشخص.")

    target = message.reply_to_message.from_user
    if target_is_protected(message.chat.id, target.id):
        return bot.reply_to(message, "❌ ما أگدر أنذر هذا الشخص.")

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
            if uid not in groups[gid]["bans"]:
                groups[gid]["bans"].append(uid)
                save_groups(groups)
            bot.reply_to(message, f"🚫 تم حظر {mention_user(target)} بعد 3 إنذارات.")
        except:
            bot.reply_to(message, f"⚠️ انذار رقم {count} لـ {mention_user(target)}")
    else:
        bot.reply_to(message, f"⚠️ انذار رقم {count} لـ {mention_user(target)}")


# =========================
# المسح
# =========================
def clear_specific_rank(message, rank_name, success_text):
    if not is_group(message):
        return
    if not has_owner_rank(message.chat.id, message.from_user.id):
        return owner_only(message)
    clear_rank(message.chat.id, rank_name)
    bot.reply_to(message, f"✅ {success_text}")


def clear_bans(message):
    if not is_group(message):
        return
    if not has_owner_rank(message.chat.id, message.from_user.id):
        return owner_only(message)

    groups = load_groups()
    gid = str(message.chat.id)
    for uid in groups[gid]["bans"][:]:
        try:
            bot.unban_chat_member(message.chat.id, int(uid), only_if_banned=False)
        except:
            pass
    groups[gid]["bans"] = []
    save_groups(groups)
    bot.reply_to(message, "✅ تم مسح المحظورين.")


def clear_mutes(message):
    if not is_group(message):
        return
    if not has_owner_rank(message.chat.id, message.from_user.id):
        return owner_only(message)

    groups = load_groups()
    gid = str(message.chat.id)
    for uid in groups[gid]["mutes"][:]:
        try:
            bot.restrict_chat_member(message.chat.id, int(uid), permissions=unmute_permissions())
        except:
            pass
    groups[gid]["mutes"] = []
    save_groups(groups)
    bot.reply_to(message, "✅ تم مسح المكتومين.")


# =========================
# القفل والفتح
# =========================
def lock_command(message, state):
    if not is_group(message):
        return
    if not has_high_rank(message.chat.id, message.from_user.id):
        return high_only(message)

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return bot.reply_to(message, "❌ اكتب الأمر بهذا الشكل: قفل الروابط")

    key = lock_name_map(parts[1].strip())
    if not key:
        return bot.reply_to(message, "❌ هذا النوع غير مدعوم حالياً.")

    set_lock(message.chat.id, key, state)
    bot.reply_to(message, f"✅ تم {'قفل' if state else 'فتح'} {parts[1].strip()}")


# =========================
# الإعدادات
# =========================
def toggle_welcome(message, value):
    if not is_group(message):
        return
    if not has_high_rank(message.chat.id, message.from_user.id):
        return high_only(message)

    groups = load_groups()
    gid = str(message.chat.id)
    groups[gid]["welcome_enabled"] = value
    save_groups(groups)
    bot.reply_to(message, f"✅ تم {'تفعيل' if value else 'تعطيل'} الترحيب.")


def set_welcome(message):
    if not is_group(message):
        return
    if not has_high_rank(message.chat.id, message.from_user.id):
        return high_only(message)

    text = message.text.replace("وضع ترحيب ", "", 1).strip()
    if not text:
        return bot.reply_to(message, "❌ اكتب النص بعد الأمر.")

    groups = load_groups()
    gid = str(message.chat.id)
    groups[gid]["welcome_text"] = text
    save_groups(groups)
    bot.reply_to(message, "✅ تم حفظ رسالة الترحيب.")


def delete_welcome(message):
    if not is_group(message):
        return
    if not has_high_rank(message.chat.id, message.from_user.id):
        return high_only(message)

    groups = load_groups()
    gid = str(message.chat.id)
    groups[gid]["welcome_text"] = "أهلاً بك {name} في {group}"
    save_groups(groups)
    bot.reply_to(message, "✅ تم حذف الترحيب المخصص.")


def set_rules(message):
    if not is_group(message):
        return
    if not has_high_rank(message.chat.id, message.from_user.id):
        return high_only(message)

    text = message.text.replace("تعيين القوانين ", "", 1).strip()
    groups = load_groups()
    groups[str(message.chat.id)]["rules"] = text
    save_groups(groups)
    bot.reply_to(message, "✅ تم حفظ القوانين.")


def delete_rules(message):
    if not is_group(message):
        return
    if not has_high_rank(message.chat.id, message.from_user.id):
        return high_only(message)

    groups = load_groups()
    groups[str(message.chat.id)]["rules"] = ""
    save_groups(groups)
    bot.reply_to(message, "✅ تم حذف القوانين.")


def show_rules(message):
    if not is_group(message):
        return
    data = get_group_data(message.chat.id)
    if not data["rules"]:
        return bot.reply_to(message, "❌ لا توجد قوانين محفوظة.")
    bot.reply_to(message, f"📜 القوانين:\n{data['rules']}")


def set_description(message):
    if not is_group(message):
        return
    if not has_high_rank(message.chat.id, message.from_user.id):
        return high_only(message)

    text = message.text.replace("تعيين وصف ", "", 1).strip()
    groups = load_groups()
    groups[str(message.chat.id)]["description"] = text
    save_groups(groups)
    bot.reply_to(message, "✅ تم حفظ الوصف.")


def show_description(message):
    if not is_group(message):
        return
    data = get_group_data(message.chat.id)
    if not data["description"]:
        return bot.reply_to(message, "❌ لا يوجد وصف محفوظ.")
    bot.reply_to(message, f"📝 الوصف:\n{data['description']}")


def show_settings(message):
    if not is_group(message):
        return
    data = get_group_data(message.chat.id)
    locks = data["locks"]

    text = (
        f"• الترحيب: {'مفعل' if data['welcome_enabled'] else 'معطل'}\n"
        f"• الروابط: {'مقفول' if locks['links'] else 'مفتوح'}\n"
        f"• المعرف: {'مقفول' if locks['username'] else 'مفتوح'}\n"
        f"• التاك: {'مقفول' if locks['tag'] else 'مفتوح'}\n"
        f"• الصور: {'مقفول' if locks['photos'] else 'مفتوح'}\n"
        f"• الفيديو: {'مقفول' if locks['video'] else 'مفتوح'}\n"
        f"• الصوت: {'مقفول' if locks['voice'] else 'مفتوح'}\n"
        f"• الصوتيات: {'مقفول' if locks['audio'] else 'مفتوح'}\n"
        f"• الملفات: {'مقفول' if locks['files'] else 'مفتوح'}\n"
        f"• الملصقات: {'مقفول' if locks['stickers'] else 'مفتوح'}\n"
        f"• المتحركة: {'مقفول' if locks['gif'] else 'مفتوح'}\n"
        f"• التوجيه: {'مقفول' if locks['forward'] else 'مفتوح'}\n"
        f"• البوتات: {'مقفول' if locks['bots'] else 'مفتوح'}\n"
        f"• الدردشة: {'مقفول' if locks['chat'] else 'مفتوح'}"
    )
    bot.reply_to(message, text)


def handle_welcome(message):
    if not is_group(message):
        return

    data = get_group_data(message.chat.id)
    if not data["welcome_enabled"]:
        return

    for member in message.new_chat_members:
        text = data["welcome_text"]
        text = text.replace("{name}", member.first_name or "عضو")
        text = text.replace("{group}", message.chat.title or "المجموعة")
        try:
            bot.send_message(message.chat.id, text)
        except:
            pass


# =========================
# Dev
# =========================
def count_users(message):
    if not is_dev(message.from_user.id):
        return bot.reply_to(message, "❌ هذا الأمر فقط للمطور.")
    users = load_users()
    bot.reply_to(message, f"👤 عدد المستخدمين: {len(users)}")


def count_groups(message):
    if not is_dev(message.from_user.id):
        return bot.reply_to(message, "❌ هذا الأمر فقط للمطور.")
    groups = load_groups()
    bot.reply_to(message, f"👥 عدد الكروبات: {len(groups)}")


def broadcast_message(message):
    if not is_dev(message.from_user.id):
        return bot.reply_to(message, "❌ هذا الأمر فقط للمطور.")
    text = message.text.replace("اذاعة ", "", 1).strip()
    if not text:
        return bot.reply_to(message, "❌ اكتب النص بعد اذاعة")

    users = load_users()
    sent = 0
    for uid in users.keys():
        try:
            bot.send_message(int(uid), text)
            sent += 1
        except:
            pass
    bot.reply_to(message, f"✅ تمت الاذاعة إلى {sent} مستخدم.")


print("Bot is running...")
bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
