import os
import json
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8516176029:AAH-s3Y0nLAdmQN_LyeR3aS-tbK1XInMINY"
RAPID_API_KEY = ""8d1aaa7799mshaeb22e8130d13c2p169c25jsnf375a4b0af2b"
 https://rapidapi.com/zayviusdigital/api/yt-search-and-download-mp3/playground/apiendpoint_ae2beb99-211c-415d-a1c0-9e0a4d6dbad8#:~:text=x%2Drapidapi%2Dkey%3A-,8d1aaa7799mshaeb22e8130d13c2p169c25jsnf375a4b0af2b,-%27"

OWNER_ID = 8065884629
BOT_USERNAME = "fadifvambot"
DEV_USERNAME = "fvamv"
FORCE_CHANNEL = "@fadifva"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "locks": {},
    "ranks": {},
    "muted": {},
    "users": {},
    "groups": {},
    "replies": {},
    "notify": True
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in DEFAULT_DATA.items():
            if k not in d:
                d[k] = v
        save_data(d)
        return d
    except:
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()
waiting_reply = {}

def chat_id_str(chat_id):
    return str(chat_id)

def user_id_str(user_id):
    return str(user_id)

def register_user(message):
    if not message.from_user:
        return

    uid = user_id_str(message.from_user.id)

    if uid not in data["users"]:
        data["users"][uid] = {
            "name": message.from_user.first_name or "",
            "username": message.from_user.username or "ماكو"
        }
        save_data(data)

        if data.get("notify", True):
            try:
                username = message.from_user.username or "ماكو"
                bot.send_message(
                    OWNER_ID,
                    f"🔔 دخول مستخدم جديد للبوت\n\n"
                    f"👤 الاسم: {message.from_user.first_name}\n"
                    f"🔗 اليوزر: {username}\n"
                    f"🆔 الايدي: {message.from_user.id}"
                )
            except:
                pass

    if message.chat.type in ["group", "supergroup"]:
        cid = chat_id_str(message.chat.id)
        if cid not in data["groups"]:
            data["groups"][cid] = {
                "title": message.chat.title or "",
                "username": message.chat.username or ""
            }
            save_data(data)

def get_locks(chat_id):
    cid = chat_id_str(chat_id)
    if cid not in data["locks"]:
        data["locks"][cid] = {
            "links": False,
            "photos": False,
            "stickers": False,
            "videos": False,
            "forward": False,
            "bots": False,
            "all": False
        }
        save_data(data)
    return data["locks"][cid]

def get_rank(chat_id, user_id):
    cid = chat_id_str(chat_id)
    uid = user_id_str(user_id)
    return data["ranks"].get(cid, {}).get(uid)

def set_rank(chat_id, user_id, rank):
    cid = chat_id_str(chat_id)
    uid = user_id_str(user_id)
    data["ranks"].setdefault(cid, {})
    data["ranks"][cid][uid] = rank
    save_data(data)

def del_rank(chat_id, user_id):
    cid = chat_id_str(chat_id)
    uid = user_id_str(user_id)
    if cid in data["ranks"] and uid in data["ranks"][cid]:
        del data["ranks"][cid][uid]
        save_data(data)

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print("SUB ERROR:", e)
        return True

def sub_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("اشترك بالقناة", url="https://t.me/fadifva"))
    return kb

def check_sub(message):
    if message.from_user and not is_subscribed(message.from_user.id):
        bot.reply_to(
            message,
            "⚠️ عزيزي لازم تشترك بقناة البوت أولاً:\nhttps://t.me/fadifva",
            reply_markup=sub_keyboard()
        )
        return False
    return True

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        if member.status in ["creator", "administrator"]:
            return True
        rank = get_rank(chat_id, user_id)
        return rank in ["مالك اساسي", "مالك", "منشئ", "مدير", "ادمن", "مشرف"]
    except:
        return False

def can_use_admin(message):
    if message.chat.type == "private":
        return False
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر للمشرفين وما فوق فقط")
        return False
    return True

def target_user(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❗ لازم ترد على رسالة الشخص")
        return None
    return message.reply_to_message.from_user

def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("1️⃣ أوامر الإدارة", callback_data="help_admin"))
    kb.add(InlineKeyboardButton("2️⃣ أوامر القفل والفتح", callback_data="help_locks"))
    kb.add(InlineKeyboardButton("3️⃣ أوامر الميوزك", callback_data="help_music"))
    kb.add(InlineKeyboardButton("4️⃣ أوامر التسليه", callback_data="help_fun"))
    kb.add(InlineKeyboardButton("5️⃣ أوامر Dev", callback_data="help_dev"))
    return kb

def owner_panel():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🟢➕ صانع الردود", callback_data="owner_add_reply"))
    kb.add(
        InlineKeyboardButton("🔵📜 الردود", callback_data="owner_replies"),
        InlineKeyboardButton("🔵👥 المستخدمين", callback_data="owner_users")
    )
    kb.add(
        InlineKeyboardButton("🔴🗑 حذف رد", callback_data="owner_del_reply"),
        InlineKeyboardButton("🔵📊 الكروبات", callback_data="owner_groups")
    )
    kb.add(InlineKeyboardButton("🟡🔔 إشعار الدخول", callback_data="owner_notify"))
    kb.add(InlineKeyboardButton("🔴 رجوع", callback_data="commands"))
    return kb

def start_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{DEV_USERNAME}"))
    kb.add(InlineKeyboardButton("➕ اضفني للكروب", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"))
    kb.add(InlineKeyboardButton("💰 شراء بوت مشابه", url=f"https://t.me/{DEV_USERNAME}"))
    kb.add(InlineKeyboardButton("📚 الأوامر", callback_data="commands"))
    return kb

HELP_ADMIN = """
<b>أوامر الإدارة</b>

• حظر بالرد
• الغاء الحظر بالرد
• طرد بالرد
• كتم بالرد
• الغاء الكتم بالرد
• مسح بالرد
• مسح 10

<b>الرتب بالرد:</b>
• رفع مالك اساسي
• رفع مالك
• رفع منشئ
• رفع مدير
• رفع ادمن
• رفع مشرف
• رفع مميز

• تنزيل مالك اساسي
• تنزيل مالك
• تنزيل منشئ
• تنزيل مدير
• تنزيل ادمن
• تنزيل مشرف
• تنزيل مميز

• رتبتي
• تنزيل الكل
"""

HELP_LOCKS = """
<b>أوامر القفل والفتح</b>

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
• قفل الكل
• فتح الكل
"""

HELP_MUSIC = """
<b>أوامر الميوزك</b>

• يوت سيف عامر شجرة
• يوت اسم الاغنية

يرسل الأغنية كصوت من API.
"""

HELP_FUN = """
<b>أوامر التسليه</b>

بالرد:
• رفع هطف
• رفع حمار
• رفع كلب
• رفع خروف
• رفع بقلبي

• تنزيل هطف
• تنزيل حمار
• تنزيل كلب
• تنزيل خروف
• تنزيل من قلبي

• زواج
• طلاق
"""

HELP_DEV = f"""
<b>أوامر Dev</b>

• سورس
• المطور
• شراء بوت مشابه
• الاوامر

المطور: @{DEV_USERNAME}
القناة: {FORCE_CHANNEL}
"""

@bot.message_handler(commands=["start"])
def start(message):
    register_user(message)

    if not check_sub(message):
        return

    if message.from_user.id == OWNER_ID:
        bot.send_message(
            message.chat.id,
            "⚙️ <b>لوحة تحكم المطور</b>\n\nاختر من الأزرار:",
            reply_markup=owner_panel()
        )
    else:
        bot.send_message(
            message.chat.id,
            "أهلاً بك في بوت فادي المطور 🌷\nاختر من الأزرار بالأسفل 👇",
            reply_markup=start_buttons()
        )

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass

    if call.data == "commands":
        bot.edit_message_text(
            "📚 قائمة أوامر بوت فادي\nاختر القسم:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )

    elif call.data == "help_admin":
        bot.edit_message_text(HELP_ADMIN, call.message.chat.id, call.message.message_id, reply_markup=main_menu())

    elif call.data == "help_locks":
        bot.edit_message_text(HELP_LOCKS, call.message.chat.id, call.message.message_id, reply_markup=main_menu())

    elif call.data == "help_music":
        bot.edit_message_text(HELP_MUSIC, call.message.chat.id, call.message.message_id, reply_markup=main_menu())

    elif call.data == "help_fun":
        bot.edit_message_text(HELP_FUN, call.message.chat.id, call.message.message_id, reply_markup=main_menu())

    elif call.data == "help_dev":
        bot.edit_message_text(HELP_DEV, call.message.chat.id, call.message.message_id, reply_markup=main_menu())

    elif call.data.startswith("owner_"):
        if call.from_user.id != OWNER_ID:
            return bot.answer_callback_query(call.id, "❌ هذه اللوحة للمطور فقط", show_alert=True)

        if call.data == "owner_add_reply":
            waiting_reply[call.from_user.id] = {"step": "add_word"}
            bot.send_message(call.message.chat.id, "✏️ اكتب الكلمة التي تريد البوت يرد عليها:\nمثال: هلو")

        elif call.data == "owner_del_reply":
            waiting_reply[call.from_user.id] = {"step": "del_word"}
            bot.send_message(call.message.chat.id, "🗑 اكتب الكلمة التي تريد حذف ردها:")

        elif call.data == "owner_replies":
            if not data["replies"]:
                txt = "📜 لا توجد ردود مضافة."
            else:
                txt = "📜 <b>الردود المضافة:</b>\n\n"
                for i, word in enumerate(data["replies"].keys(), 1):
                    txt += f"{i}. {word}\n"
            bot.send_message(call.message.chat.id, txt)

        elif call.data == "owner_users":
            txt = f"👥 عدد المستخدمين: {len(data['users'])}\n\n"
            for uid, info in list(data["users"].items())[-20:]:
                username = info.get("username") or "ماكو"
                name = info.get("name") or "بدون"
                txt += f"• {name} | {username} | <code>{uid}</code>\n"
            bot.send_message(call.message.chat.id, txt)

        elif call.data == "owner_groups":
            txt = f"📊 عدد الكروبات: {len(data['groups'])}\n\n"
            for cid, info in data["groups"].items():
                title = info.get("title") or "بدون اسم"
                username = info.get("username")
                link = f"https://t.me/{username}" if username else "لا يوجد رابط عام"
                txt += f"• {title}\n{link}\n<code>{cid}</code>\n\n"
            bot.send_message(call.message.chat.id, txt)

        elif call.data == "owner_notify":
            data["notify"] = not data.get("notify", True)
            save_data(data)
            status = "مفعل ✅" if data["notify"] else "متوقف ❌"
            bot.send_message(call.message.chat.id, f"🔔 إشعار الدخول: {status}")

@bot.message_handler(content_types=["new_chat_members"])
def welcome(message):
    register_user(message)

    for u in message.new_chat_members:
        if u.is_bot:
            locks = get_locks(message.chat.id)
            if locks.get("bots"):
                try:
                    bot.ban_chat_member(message.chat.id, u.id)
                except:
                    pass
                continue

        bot.send_message(
            message.chat.id,
            f"هلا {u.first_name} 🌷\nنورت الكروب\nالتزم بالقوانين وتقدر تشارك برأيك بكل احترام.",
            reply_markup=start_buttons()
        )

@bot.message_handler(content_types=["text", "photo", "video", "sticker", "document", "audio", "voice"])
def handler(message):
    register_user(message)

    if message.chat.type != "private":
        if not check_sub(message):
            return

    locks = get_locks(message.chat.id)
    text = message.text or ""

    if message.chat.type != "private":
        if locks.get("all") and not is_admin(message.chat.id, message.from_user.id):
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            return

        if locks.get("links") and text and ("http://" in text or "https://" in text or "t.me/" in text):
            if not is_admin(message.chat.id, message.from_user.id):
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except:
                    pass
                return

        if locks.get("photos") and message.content_type == "photo" and not is_admin(message.chat.id, message.from_user.id):
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            return

        if locks.get("videos") and message.content_type == "video" and not is_admin(message.chat.id, message.from_user.id):
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            return

        if locks.get("stickers") and message.content_type == "sticker" and not is_admin(message.chat.id, message.from_user.id):
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            return

        if locks.get("forward") and message.forward_date and not is_admin(message.chat.id, message.from_user.id):
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            return

    if not text:
        return

    if message.from_user.id in waiting_reply:
        state = waiting_reply[message.from_user.id]

        if state["step"] == "add_word":
            waiting_reply[message.from_user.id] = {"step": "add_answer", "word": text}
            bot.reply_to(message, "💬 هسه اكتب الرد على هاي الكلمة:")

        elif state["step"] == "add_answer":
            word = state["word"]
            data["replies"][word] = text
            save_data(data)
            del waiting_reply[message.from_user.id]
            bot.reply_to(message, f"✅ تم إضافة رد جديد:\nالكلمة: {word}\nالرد: {text}")

        elif state["step"] == "del_word":
            if text in data["replies"]:
                del data["replies"][text]
                save_data(data)
                bot.reply_to(message, f"✅ تم حذف الرد على: {text}")
            else:
                bot.reply_to(message, "❌ ماكو رد محفوظ على هاي الكلمة")
            del waiting_reply[message.from_user.id]

        return

    if text in data["replies"]:
        bot.reply_to(message, data["replies"][text])
        return

    if text in ["لوحة", "لوحه", "panel"] and message.from_user.id == OWNER_ID:
        bot.reply_to(message, "⚙️ لوحة تحكم المطور", reply_markup=owner_panel())

    elif text in ["الاوامر", "الأوامر", "اوامر"]:
        bot.reply_to(message, "📚 اختر قسم الأوامر:", reply_markup=main_menu())

    elif text == "سورس":
        bot.reply_to(message, "أهلاً بك في سورس فادي 🔥")

    elif text == "المطور":
        bot.reply_to(message, f"👨‍💻 المطور: @{DEV_USERNAME}")

    elif text == "شراء بوت مشابه":
        bot.reply_to(message, f"💰 للشراء راسل المطور: @{DEV_USERNAME}")

    elif text == "رتبتي":
        rank = get_rank(message.chat.id, message.from_user.id)
        bot.reply_to(message, f"رتبتك: {rank or 'عضو'}")

    elif text in ["حظر", "طرد", "كتم", "الغاء الكتم", "الغاء الحظر"]:
        if not can_use_admin(message):
            return
        user = target_user(message)
        if not user:
            return

        try:
            if text == "حظر":
                bot.ban_chat_member(message.chat.id, user.id)
                bot.reply_to(message, "✅ تم حظر العضو")

            elif text == "الغاء الحظر":
                bot.unban_chat_member(message.chat.id, user.id)
                bot.reply_to(message, "✅ تم إلغاء الحظر")

            elif text == "طرد":
                bot.ban_chat_member(message.chat.id, user.id)
                bot.unban_chat_member(message.chat.id, user.id)
                bot.reply_to(message, "✅ تم طرد العضو")

            elif text == "كتم":
                bot.restrict_chat_member(message.chat.id, user.id, can_send_messages=False)
                data["muted"].setdefault(chat_id_str(message.chat.id), [])
                if user_id_str(user.id) not in data["muted"][chat_id_str(message.chat.id)]:
                    data["muted"][chat_id_str(message.chat.id)].append(user_id_str(user.id))
                save_data(data)
                bot.reply_to(message, "✅ تم كتم العضو")

            elif text == "الغاء الكتم":
                bot.restrict_chat_member(
                    message.chat.id,
                    user.id,
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
                cid = chat_id_str(message.chat.id)
                if cid in data["muted"] and user_id_str(user.id) in data["muted"][cid]:
                    data["muted"][cid].remove(user_id_str(user.id))
                    save_data(data)
                bot.reply_to(message, "✅ تم إلغاء الكتم")

        except Exception as e:
            print("ADMIN ERROR:", e)
            bot.reply_to(message, "❌ فشل الأمر، تأكد البوت مشرف وعنده صلاحيات")

    elif text == "مسح" or text == "مسح بالرد":
        if not can_use_admin(message):
            return
        if message.reply_to_message:
            try:
                bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                bot.delete_message(message.chat.id, message.message_id)
            except:
                bot.reply_to(message, "❌ ما اكدر أمسح، تأكد من صلاحيات البوت")
        else:
            bot.reply_to(message, "رد على رسالة حتى أمسحها")

    elif text.startswith("مسح "):
        if not can_use_admin(message):
            return
        try:
            count = int(text.split()[1])
            count = min(count, 100)
            for i in range(count + 1):
                try:
                    bot.delete_message(message.chat.id, message.message_id - i)
                except:
                    pass
        except:
            bot.reply_to(message, "اكتب هكذا: مسح 10")

    elif text.startswith("رفع "):
        if not can_use_admin(message):
            return
        user = target_user(message)
        if not user:
            return
        rank = text.replace("رفع ", "").strip()
        allowed = ["مالك اساسي", "مالك", "منشئ", "مدير", "ادمن", "مشرف", "مميز", "هطف", "حمار", "كلب", "خروف", "بقلبي"]
        if rank not in allowed:
            return bot.reply_to(message, "❌ هذه الرتبة غير موجودة")
        set_rank(message.chat.id, user.id, rank)
        bot.reply_to(message, f"✅ تم رفعه {rank}")

    elif text.startswith("تنزيل "):
        if not can_use_admin(message):
            return
        user = target_user(message)
        if not user:
            return
        del_rank(message.chat.id, user.id)
        bot.reply_to(message, "✅ تم تنزيل رتبته")

    elif text == "تنزيل الكل":
        if not can_use_admin(message):
            return
        cid = chat_id_str(message.chat.id)
        data["ranks"][cid] = {}
        save_data(data)
        bot.reply_to(message, "✅ تم تنزيل كل الرتب")

    elif text.startswith("قفل "):
        if not can_use_admin(message):
            return
        name = text.replace("قفل ", "").strip()
        mapping = {
            "الروابط": "links",
            "الصور": "photos",
            "الفيديو": "videos",
            "الملصقات": "stickers",
            "التوجيه": "forward",
            "البوتات": "bots",
            "الكل": "all"
        }
        if name in mapping:
            locks[mapping[name]] = True
            save_data(data)
            bot.reply_to(message, f"🔒 تم قفل {name}")
        else:
            bot.reply_to(message, "❌ هذا القفل غير موجود")

    elif text.startswith("فتح "):
        if not can_use_admin(message):
            return
        name = text.replace("فتح ", "").strip()
        mapping = {
            "الروابط": "links",
            "الصور": "photos",
            "الفيديو": "videos",
            "الملصقات": "stickers",
            "التوجيه": "forward",
            "البوتات": "bots",
            "الكل": "all"
        }
        if name in mapping:
            locks[mapping[name]] = False
            save_data(data)
            bot.reply_to(message, f"🔓 تم فتح {name}")
        else:
            bot.reply_to(message, "❌ هذا الفتح غير موجود")

    elif text in ["زواج", "طلاق"]:
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على شخص حتى يتم الأمر")
        if text == "زواج":
            bot.reply_to(message, f"💍 تم الزواج بينك وبين {message.reply_to_message.from_user.first_name}")
        else:
            bot.reply_to(message, "💔 تم الطلاق بنجاح")

    elif text.startswith("يوت "):
        query = text.replace("يوت ", "").strip()
        if not query:
            return bot.reply_to(message, "اكتب اسم الأغنية بعد يوت")

        wait = bot.reply_to(message, "🔎 جاري البحث عن الأغنية...")

        try:
            url = "https://yt-search-and-download-mp3.p.rapidapi.com/mp3"

            headers = {
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": "yt-search-and-download-mp3.p.rapidapi.com"
            }

            params = {"q": query}

            res = requests.get(url, headers=headers, params=params, timeout=60)
            api_data = res.json()

            print("API RESPONSE:", api_data)

            audio_url = (
                api_data.get("link")
                or api_data.get("url")
                or api_data.get("audio")
                or api_data.get("download")
            )

            title = api_data.get("title") or query

            if not audio_url:
                return bot.reply_to(message, "❌ ما حصلت رابط الصوت من الـ API")

            try:
                bot.delete_message(message.chat.id, wait.message_id)
            except:
                pass

            bot.send_audio(
                message.chat.id,
                audio_url,
                title=title,
                performer="Aurelius"
            )

        except Exception as e:
            print("API MUSIC ERROR:", e)
            bot.reply_to(message, "❌ صار خطأ أثناء جلب الأغنية من API")


print("Aurelius bot is running...")
bot.infinity_polling(skip_pending=True)
